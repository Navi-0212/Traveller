import os
import json
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models import TravelConstraints, LogisticsOutput, BudgetOutput, ReviewOutput

load_dotenv()

class ReviewAgent:
    def __init__(self, client: Optional[genai.Client] = None):
        self.client = client or genai.Client()
        self.model_name = "gemini-2.5-flash-lite"

    def validate_itinerary(
        self,
        constraints: TravelConstraints,
        itinerary: LogisticsOutput,
        budget: BudgetOutput
    ) -> ReviewOutput:
        system_instruction = (
            "You are the Review Agent for Traveller. Your task is to serve as the quality assurance gate. "
            "You will audit the generated itinerary and budget details against the original constraints.\n\n"
            "Evaluate these checks and output the status ('PASS' or 'FAIL'), failure reasons (if FAIL), "
            "and a dictionary representation of the checklist. The checklist must check:\n"
            "1. duration_fit: True if the itinerary has exactly the duration specified in constraints.\n"
            "2. city_coverage: True if all requested cities are represented in the day-by-day plan.\n"
            "3. budget_compliance: True if total estimated costs across all budget categories are less than or equal to the total budget limit.\n"
            "4. preference_alignment: True if activities align with the user's positive preferences.\n"
            "5. avoidance_compliance: True if recommendations strictly respect user avoidances (e.g., no crowded spots scheduled during peak hours if they hate crowds).\n"
            "6. logistics_realism: True if active hours per day are realistic (typically <= 9 hours) and geographic sequencing prevents backtracking.\n\n"
            "Fail the validation (set status to 'FAIL') if ANY critical checklist item is False, and describe exactly what failed in 'failure_reason'."
        )

        # Build raw details representation for the prompt
        itinerary_str = ""
        for day in itinerary.days:
            itinerary_str += f"Day {day.day_number}: {day.title}\n"
            for act in day.activities:
                itinerary_str += (
                    f"  - {act.name} ({act.type}) - Slot: {act.time_slot}, "
                    f"Cost: ${act.cost_usd}, Duration: {act.duration_hours}h, Crowd: {act.crowd_level}, Info: {act.description}\n"
                )
            if day.transit_info:
                itinerary_str += f"  - Transit: {day.transit_info}\n"

        budget_str = ""
        total_estimated = 0.0
        for b in budget.budget_summary:
            budget_str += f"- {b.category}: Allocated: ${b.allocated_usd}, Estimated: ${b.estimated_cost_usd}, Status: {b.status}\n"
            total_estimated += b.estimated_cost_usd

        prompt = (
            f"--- TRAVEL CONSTRAINTS ---\n"
            f"Destination: {constraints.destination}\n"
            f"Cities: {', '.join(constraints.cities)}\n"
            f"Duration: {constraints.duration_days} days\n"
            f"Budget Limit: ${constraints.budget_usd}\n"
            f"Preferences: {', '.join(constraints.preferences)}\n"
            f"Avoidances: {', '.join(constraints.avoidances)}\n\n"
            f"--- GENERATED ITINERARY ---\n"
            f"{itinerary_str}\n"
            f"--- BUDGET BREAKDOWN ---\n"
            f"{budget_str}\n"
            f"Total Estimated Cost: ${total_estimated}"
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=ReviewOutput,
                    temperature=0.3,
                )
            )
            
            if hasattr(response, "parsed") and response.parsed is not None:
                return response.parsed
            
            data = json.loads(response.text)
            return ReviewOutput(**data)
            
        except Exception as e:
            raise ValueError(f"Failed to validate itinerary: {str(e)}")
