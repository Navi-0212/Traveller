import logging
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

from google import genai
from app.models import ItineraryPlan, TravelConstraints
from app.agents.orchestrator import OrchestratorAgent
from app.agents.destination import DestinationResearchAgent
from app.agents.logistics import LogisticsAgent
from app.agents.budget import BudgetAgent
from app.agents.review import ReviewAgent
from app.agents.refiner import RefinerAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ItineraryPipeline:
    def __init__(self, client: Optional[genai.Client] = None):
        self.client = client or genai.Client()
        self.orchestrator = OrchestratorAgent(client=self.client)
        self.destination = DestinationResearchAgent(client=self.client)
        self.logistics = LogisticsAgent(client=self.client)
        self.budget_agent = BudgetAgent(client=self.client)
        self.review_agent = ReviewAgent(client=self.client)
        self.refiner = RefinerAgent(client=self.client)

    def generate_plan(self, user_prompt: Optional[str] = None, constraints: Optional[TravelConstraints] = None) -> ItineraryPlan:
        if constraints is None:
            if user_prompt is None:
                raise ValueError("Must provide either user_prompt or constraints")
            logger.info(f"Starting plan generation for prompt: {user_prompt}")
            # 1. Orchestrator extracts travel constraints
            constraints = self.orchestrator.extract_constraints(user_prompt)
        else:
            logger.info(f"Starting plan generation directly from constraints: {constraints}")
        
        logger.info(f"Extracted constraints: {constraints}")
        
        retries = 0
        max_retries = 2
        feedback = ""
        
        last_itinerary = None
        last_budget = None
        last_review = None
        
        while retries <= max_retries:
            logger.info(f"Execution loop {retries + 1}/{max_retries + 1}")
            try:
                # 2. Destination Research Agent curates spots
                curation = self.destination.curate_destination(constraints, feedback)
                
                # 3. Logistics Agent sequences day-by-day
                itinerary = self.logistics.sequence_itinerary(constraints, curation, feedback)
                last_itinerary = itinerary
                
                # 4. Budget Agent models costs
                budget = self.budget_agent.calculate_budget(constraints, itinerary)
                last_budget = budget
                
                # 5. Review Agent validates compliance
                review = self.review_agent.validate_itinerary(constraints, itinerary, budget)
                last_review = review
                
                if review.status == "PASS":
                    logger.info("Review Agent passed. Returning successful itinerary.")
                    return ItineraryPlan(
                        destination=constraints.destination,
                        duration_days=constraints.duration_days,
                        days=itinerary.days,
                        budget_summary=budget.budget_summary,
                        validation_passed=True,
                        validation_notes=f"Successfully validated by Review Agent. Attempt: {retries + 1}."
                    )
                else:
                    logger.warning(f"Review Agent failed: {review.failure_reason}")
                    feedback = f"Your previous generation failed quality checks: {review.failure_reason}"
                    retries += 1
            except Exception as e:
                logger.error(f"Error in execution loop: {str(e)}")
                retries += 1
                feedback = f"Previous attempt failed with error: {str(e)}. Please correct structures and ensure valid outputs."

        # If retries exhausted and validation fails, return what we have with validation_passed=False
        logger.error("Failed to pass Review Agent checks within retry limits. Returning partial plan.")
        return ItineraryPlan(
            destination=constraints.destination,
            duration_days=constraints.duration_days,
            days=last_itinerary.days if last_itinerary else [],
            budget_summary=last_budget.budget_summary if last_budget else [],
            validation_passed=False,
            validation_notes=f"Validation failed after {max_retries + 1} attempts: {last_review.failure_reason if last_review else 'Agent execution error.'}"
        )

    def refine_plan(self, existing_plan: ItineraryPlan, instructions: str) -> ItineraryPlan:
        logger.info(f"Starting itinerary refinement. Instructions: {instructions}")
        
        try:
            # 1. Refiner edits the logistics itinerary plan structure
            updated_itinerary = self.refiner.refine_itinerary(existing_plan, instructions)
            
            # Recreate constraints from the existing plan to check budget
            total_budget = sum(b.allocated_usd for b in existing_plan.budget_summary)
            if total_budget == 0:
                total_budget = 2000.0  # Safe default if not specified
                
            constraints = TravelConstraints(
                destination=existing_plan.destination,
                cities=[existing_plan.destination],
                duration_days=existing_plan.duration_days,
                budget_usd=total_budget,
                preferences=["refinement"],
                avoidances=[]
            )
            
            # 2. Re-calculate budget
            updated_budget = self.budget_agent.calculate_budget(constraints, updated_itinerary)
            
            # 3. Re-run Review Agent check
            review = self.review_agent.validate_itinerary(constraints, updated_itinerary, updated_budget)
            
            return ItineraryPlan(
                destination=existing_plan.destination,
                duration_days=existing_plan.duration_days,
                days=updated_itinerary.days,
                budget_summary=updated_budget.budget_summary,
                validation_passed=(review.status == "PASS"),
                validation_notes=f"Refinement processed. Validation status: {review.status}. Notes: {review.failure_reason if review.status == 'FAIL' else 'None'}"
            )
        except Exception as e:
            logger.error(f"Failed to refine itinerary: {str(e)}")
            # Return original plan with failure validation notes
            return ItineraryPlan(
                destination=existing_plan.destination,
                duration_days=existing_plan.duration_days,
                days=existing_plan.days,
                budget_summary=existing_plan.budget_summary,
                validation_passed=False,
                validation_notes=f"Failed to apply refinement instructions: {str(e)}"
            )
