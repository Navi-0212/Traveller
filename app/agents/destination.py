import os
import json
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models import TravelConstraints, DestinationCuration

from app.utils import call_gemini_with_retry

load_dotenv()

class DestinationResearchAgent:
    def __init__(self, client: Optional[genai.Client] = None):
        self.client = client or genai.Client()
        self.model_name = "gemini-2.5-flash-lite"

    def curate_destination(self, constraints: TravelConstraints, feedback: Optional[str] = None) -> DestinationCuration:
        system_instruction = (
            "You are the Destination Research Agent for Traveller. Your role is to discover and "
            "curate places, experiences, and dining options that match the traveler's constraints.\n\n"
            "Analyze the destination, cities to visit, preferences, and avoidances.\n"
            "Suggest recommended places (attractions, restaurants, scenic spots) with neighborhood "
            "details, category, cost, and time required. Also suggest neighborhoods to stay in.\n\n"
            "Adhere strictly to preferences and avoidances:\n"
            "- If they hate crowds, recommend lesser-known, quieter alternatives (e.g., Nezu Shrine instead of Meiji Jingu in Tokyo, or Otagi Nenbutsu-ji in Kyoto).\n"
            "- If they love food, ensure a rich set of local dining options are recommended.\n"
            "- Ensure the recommendations cover all requested cities."
        )

        prompt = (
            f"Destination: {constraints.destination}\n"
            f"Cities: {', '.join(constraints.cities)}\n"
            f"Duration: {constraints.duration_days} days\n"
            f"Preferences: {', '.join(constraints.preferences)}\n"
            f"Avoidances: {', '.join(constraints.avoidances)}\n"
            f"Accommodation Tier: {constraints.accommodation_preference}"
        )

        if feedback:
            prompt += f"\n\nCRITICAL FEEDBACK FROM PREVIOUS RUN:\n{feedback}\nPlease adjust the curation specifically to fix these validation errors."

        try:
            response = call_gemini_with_retry(
                client=self.client,
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=DestinationCuration,
                    temperature=0.7,
                )
            )
            
            if hasattr(response, "parsed") and response.parsed is not None:
                return response.parsed
            
            data = json.loads(response.text)
            return DestinationCuration(**data)
            
        except Exception as e:
            raise ValueError(f"Failed to curate destination: {str(e)}")
