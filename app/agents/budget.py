import os
import json
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models import TravelConstraints, LogisticsOutput, BudgetOutput

load_dotenv()

class BudgetAgent:
    def __init__(self, client: Optional[genai.Client] = None):
        self.client = client or genai.Client()
        self.model_name = "gemini-2.5-flash-lite"

    def calculate_budget(
        self, constraints: TravelConstraints, itinerary: LogisticsOutput
    ) -> BudgetOutput:
        system_instruction = (
            "You are the Budget Agent for Traveller. Your task is to calculate a category-by-category "
            "financial model of the trip and compare it with the traveler's constraints.\n\n"
            "Analyze the constraints and day-by-day itinerary. Distribute the total budget and calculate "
            "estimated costs for the following categories:\n"
            "- flights (allocate 0 if not explicitly requested or implied, or standard flight cost)\n"
            "- accommodation (based on duration_days - 1 nights and accommodation_preference)\n"
            "- transit (local trains, buses, inter-city trains mentioned in transit_info)\n"
            "- food (meals, market snacks based on duration_days)\n"
            "- activities (sum of individual entry fees or experience costs of activities in the itinerary)\n"
            "- buffer (typically 10% of total budget)\n\n"
            "Budget Rules:\n"
            "1. Allocate budget target values based on standard splits for the budget tier.\n"
            "2. Sum up the activity costs from the activities in the itinerary. Do not make up arbitrary activity costs.\n"
            "3. If the estimated cost for any category exceeds its allocated target, set status to 'Exceeded'. Otherwise 'Within'.\n"
            "4. The sum of estimated costs should ideally stay within the total budget constraint."
        )

        # Convert itinerary and constraints into a text prompt representation
        itinerary_str = ""
        for day in itinerary.days:
            itinerary_str += f"Day {day.day_number}: {day.title}\n"
            for act in day.activities:
                itinerary_str += f"  - Activity: {act.name}, Cost: ${act.cost_usd}\n"
            if day.transit_info:
                itinerary_str += f"  - Transit: {day.transit_info}\n"

        prompt = (
            f"Total Budget: ${constraints.budget_usd}\n"
            f"Trip Duration: {constraints.duration_days} days\n"
            f"Accommodation Preference: {constraints.accommodation_preference}\n"
            f"Cities: {', '.join(constraints.cities)}\n"
            f"Generated Itinerary:\n{itinerary_str}"
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=BudgetOutput,
                    temperature=0.3,
                )
            )
            
            if hasattr(response, "parsed") and response.parsed is not None:
                return response.parsed
            
            data = json.loads(response.text)
            return BudgetOutput(**data)
            
        except Exception as e:
            raise ValueError(f"Failed to calculate budget: {str(e)}")
