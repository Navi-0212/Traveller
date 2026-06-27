import os
import pytest
from unittest.mock import MagicMock
from app.pipeline import ItineraryPipeline
from app.models import (
    TravelConstraints, DestinationCuration, RecommendedPlace,
    LogisticsOutput, DayItinerary, Activity, BudgetOutput,
    BudgetBreakdown, ReviewOutput, ItineraryPlan
)

# Check if GEMINI_API_KEY is configured in the environment
API_KEY_PRESENT = os.getenv("GEMINI_API_KEY") not in [None, "", "YOUR_GEMINI_API_KEY_HERE"]

def test_pipeline_generate_success_mocked():
    """Test pipeline generation success with mocked agent responses."""
    mock_client = MagicMock()
    pipeline = ItineraryPipeline(client=mock_client)
    
    # Mock Orchestrator
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=1,
        budget_usd=1000.0,
        preferences=["temples"],
        avoidances=["crowds"]
    )
    pipeline.orchestrator.extract_constraints = MagicMock(return_value=constraints)
    
    # Mock Destination Research
    curation = DestinationCuration(
        places=[
            RecommendedPlace(
                name="Nezu Shrine",
                type="temple",
                neighborhood="Yanaka",
                description="Quiet shrine",
                crowd_level="low",
                estimated_cost_usd=5.0,
                estimated_duration_hours=1.0
            )
        ],
        stay_neighborhoods=["Yanaka"]
    )
    pipeline.destination.curate_destination = MagicMock(return_value=curation)
    
    # Mock Logistics
    itinerary = LogisticsOutput(
        days=[
            DayItinerary(
                day_number=1,
                title="Quiet Day",
                activities=[
                    Activity(
                        name="Nezu Shrine",
                        type="temple",
                        time_slot="Morning",
                        cost_usd=5.0,
                        duration_hours=1.0,
                        crowd_level="low",
                        description="Quiet shrine"
                    )
                ],
                transit_info="Walk"
            )
        ]
    )
    pipeline.logistics.sequence_itinerary = MagicMock(return_value=itinerary)
    
    # Mock Budget
    budget = BudgetOutput(
        budget_summary=[
            BudgetBreakdown(
                category="activities",
                allocated_usd=100.0,
                estimated_cost_usd=5.0,
                status="Within"
            )
        ]
    )
    pipeline.budget_agent.calculate_budget = MagicMock(return_value=budget)
    
    # Mock Review (PASS)
    review = ReviewOutput(
        status="PASS",
        failure_reason=None,
        validation_checklist={"duration_fit": True, "budget_compliance": True}
    )
    pipeline.review_agent.validate_itinerary = MagicMock(return_value=review)
    
    # Run pipeline
    plan = pipeline.generate_plan("Plan a 1-day trip to Tokyo")
    
    assert plan.destination == "Japan"
    assert plan.duration_days == 1
    assert plan.validation_passed is True
    assert len(plan.days) == 1
    assert plan.days[0].activities[0].name == "Nezu Shrine"
    assert len(plan.budget_summary) == 1

def test_pipeline_retry_loop_mocked():
    """Test pipeline retry feedback loop when Review Agent fails initially."""
    mock_client = MagicMock()
    pipeline = ItineraryPipeline(client=mock_client)
    
    # Set up mocks
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=1,
        budget_usd=100.0,
        preferences=[],
        avoidances=[]
    )
    pipeline.orchestrator.extract_constraints = MagicMock(return_value=constraints)
    
    curation = DestinationCuration(places=[], stay_neighborhoods=[])
    pipeline.destination.curate_destination = MagicMock(return_value=curation)
    
    itinerary = LogisticsOutput(days=[])
    pipeline.logistics.sequence_itinerary = MagicMock(return_value=itinerary)
    
    budget = BudgetOutput(budget_summary=[])
    pipeline.budget_agent.calculate_budget = MagicMock(return_value=budget)
    
    # Mock Review Agent to FAIL first, then PASS on retry
    review_fail = ReviewOutput(
        status="FAIL",
        failure_reason="Itinerary is empty",
        validation_checklist={"duration_fit": False}
    )
    review_pass = ReviewOutput(
        status="PASS",
        failure_reason=None,
        validation_checklist={"duration_fit": True}
    )
    
    pipeline.review_agent.validate_itinerary = MagicMock(side_effect=[review_fail, review_pass])
    
    # Run pipeline
    plan = pipeline.generate_plan("Plan a 1-day trip")
    
    assert plan.validation_passed is True
    assert pipeline.review_agent.validate_itinerary.call_count == 2
    assert "Attempt: 2" in plan.validation_notes

@pytest.mark.skipif(not API_KEY_PRESENT, reason="GEMINI_API_KEY not found in environment")
def test_pipeline_live_e2e():
    """Live E2E integration test for the full generation and refinement pipeline."""
    pipeline = ItineraryPipeline()
    prompt = "Plan a 2-day foodie weekend in Tokyo under $500. Avoid crowds."
    
    plan = pipeline.generate_plan(prompt)
    assert plan.destination != ""
    assert plan.duration_days == 2
    assert len(plan.days) == 2
    assert len(plan.budget_summary) > 0
    
    # Test refinement on the generated plan
    refinement_instructions = "Add a quiet morning walking trail to Day 2."
    refined_plan = pipeline.refine_plan(plan, refinement_instructions)
    
    assert refined_plan.duration_days == 2
    assert len(refined_plan.days) == 2
