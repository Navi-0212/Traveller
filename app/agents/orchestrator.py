import os
import json
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models import TravelConstraints

load_dotenv()

class OrchestratorAgent:
    def __init__(self, client: Optional[genai.Client] = None):
        # Uses GEMINI_API_KEY from environment or loaded .env file
        self.client = client or genai.Client()
        self.model_name = "gemini-2.5-flash-lite"

    def extract_constraints(self, user_prompt: str) -> TravelConstraints:
        system_instruction = (
            "You are the Master Orchestrator Agent for Traveller. Your task is to extract "
            "structured travel constraints from a natural-language travel request.\n\n"
            "Identify the main destination, list of cities, trip duration in days, total budget "
            "in USD, preferences (what they love/want to do), avoidances (what they hate/want to avoid), "
            "implied travel style, and accommodation preference.\n\n"
            "If some details are missing, apply sensible defaults:\n"
            "- If budget is missing, default to 2000 USD.\n"
            "- If duration is missing, default to 7 days.\n"
            "- If accommodation preference is missing, default to 'mid-range'.\n"
            "- If travel style is missing, default to 'independent'.\n"
            "- If cities are missing, deduce the most common hubs for the destination (e.g. Tokyo + Kyoto for Japan)."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=TravelConstraints,
                    temperature=0.3,
                )
            )
            
            # The SDK parses the schema into response.parsed if a Pydantic class is provided
            if hasattr(response, "parsed") and response.parsed is not None:
                return response.parsed
            
            # Fallback manual parsing if parsed attribute is missing
            data = json.loads(response.text)
            return TravelConstraints(**data)
            
        except Exception as e:
            # Propagate or wrap exception for error handling
            raise ValueError(f"Failed to extract constraints: {str(e)}")
