import os
import json
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models import ItineraryPlan, LogisticsOutput

from app.utils import call_gemini_with_retry

load_dotenv()

class RefinerAgent:
    def __init__(self, client: Optional[genai.Client] = None):
        self.client = client or genai.Client()
        self.model_name = "gemini-2.5-flash-lite"

    def refine_itinerary(self, existing_plan: ItineraryPlan, instructions: str) -> LogisticsOutput:
        system_instruction = (
            "You are the Refinement Agent for Traveller. Your task is to modify an existing travel itinerary "
            "based on the user's natural language instructions.\n\n"
            "Analyze the existing itinerary plan and the user's requested modifications. Make precise adjustments "
            "to the activities, durations, slots (Morning/Afternoon/Evening), or order of days while keeping "
            "all other parts of the plan intact unless requested otherwise.\n\n"
            "Return the complete updated day-by-day itinerary matching the LogisticsOutput schema."
        )

        # Convert existing plan days to a list of dicts for prompting
        days_data = []
        for day in existing_plan.days:
            acts = []
            for act in day.activities:
                acts.append({
                    "name": act.name,
                    "type": act.type,
                    "time_slot": act.time_slot,
                    "cost_usd": act.cost_usd,
                    "duration_hours": act.duration_hours,
                    "crowd_level": act.crowd_level,
                    "description": act.description
                })
            days_data.append({
                "day_number": day.day_number,
                "title": day.title,
                "activities": acts,
                "transit_info": day.transit_info
            })

        prompt = (
            f"--- EXISTING ITINERARY ---\n"
            f"{json.dumps(days_data, indent=2)}\n\n"
            f"--- USER MODIFICATION INSTRUCTIONS ---\n"
            f"{instructions}"
        )

        try:
            response = call_gemini_with_retry(
                client=self.client,
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=LogisticsOutput,
                    temperature=0.3,
                )
            )
            
            if hasattr(response, "parsed") and response.parsed is not None:
                return response.parsed
            
            data = json.loads(response.text)
            return LogisticsOutput(**data)
            
        except Exception as e:
            raise ValueError(f"Failed to refine itinerary: {str(e)}")
