import os
import json
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models import TravelConstraints, DestinationCuration, LogisticsOutput

from app.utils import call_gemini_with_retry

load_dotenv()

class LogisticsAgent:
    def __init__(self, client: Optional[genai.Client] = None):
        self.client = client or genai.Client()
        self.model_name = "gemini-2.5-flash-lite"

    def sequence_itinerary(
        self, constraints: TravelConstraints, curation: DestinationCuration, feedback: Optional[str] = None
    ) -> LogisticsOutput:
        system_instruction = (
            "You are the Logistics Agent for Traveller. Your task is to organize recommended places "
            "into a day-by-day structured itinerary.\n\n"
            "Analyze the travel constraints and recommended places curation. Organize the activities "
            "chronologically across the trip days. For each day, specify:\n"
            "- A title representing the theme of the day.\n"
            "- Three activity blocks: 'Morning', 'Afternoon', and 'Evening' based on the recommended places.\n"
            "- Transit information between the slots (e.g., walk times, train route details).\n\n"
            "Logistics Rules:\n"
            "1. You must organize exactly the number of days specified in TravelConstraints.duration_days.\n"
            "2. Group activities geographically: places in the same neighborhood should be scheduled on the same day to minimize backtracking.\n"
            "3. Ensure the schedule is realistic (e.g., don't put three far-away spots on the same day, leave room for transit).\n"
            "4. Transit connectors should specify estimated time and cost (e.g. 'Walk (10 mins)' or 'Train (15 mins, $2)')."
        )

        # Convert curation and constraints into format for the prompt
        places_str = ""
        for place in curation.places:
            places_str += (
                f"- Name: {place.name}\n"
                f"  Type: {place.type}\n"
                f"  Neighborhood: {place.neighborhood}\n"
                f"  Vibe: {place.description}\n"
                f"  Crowd Level: {place.crowd_level}\n"
                f"  Cost: ${place.estimated_cost_usd}\n"
                f"  Duration: {place.estimated_duration_hours}h\n\n"
            )

        prompt = (
            f"Trip Duration: {constraints.duration_days} days\n"
            f"Cities to visit: {', '.join(constraints.cities)}\n"
            f"Stay Neighborhoods: {', '.join(curation.stay_neighborhoods)}\n"
            f"Available places to schedule:\n{places_str}"
        )

        if feedback:
            prompt += f"\n\nCRITICAL FEEDBACK FROM PREVIOUS RUN:\n{feedback}\nPlease adjust the sequencing and day assignments specifically to fix these validation errors."

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
            raise ValueError(f"Failed to sequence itinerary: {str(e)}")
