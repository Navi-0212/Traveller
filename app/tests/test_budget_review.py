import os
import pytest
from unittest.mock import MagicMock
from app.agents.budget import BudgetAgent
from app.agents.review import ReviewAgent
from app.models import TravelConstraints, LogisticsOutput, DayItinerary, Activity, BudgetOutput, BudgetBreakdown, ReviewOutput

# Check if GEMINI_API_KEY is configured in the environment
API_KEY_PRESENT = os.getenv("GEMINI_API_KEY") not in [None, "", "YOUR_GEMINI_API_KEY_HERE"]

def test_budget_agent_mocked():
    """Test BudgetAgent with mocked API responses."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    expected_budget = BudgetOutput(
        budget_summary=[
            BudgetBreakdown(
                category="accommodation",
                allocated_usd=600.0,
                estimated_cost_usd=550.0,
                status="Within"
            ),
            BudgetBreakdown(
                category="food",
                allocated_usd=300.0,
                estimated_cost_usd=350.0,
                status="Exceeded"
            )
        ]
    )
    
    mock_response.parsed = expected_budget
    mock_client.models.generate_content.return_value = mock_response
    
    agent = BudgetAgent(client=mock_client)
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=5,
        budget_usd=1000.0,
        preferences=["food"],
        avoidances=["crowds"]
    )
    itinerary = LogisticsOutput(
        days=[
            DayItinerary(
                day_number=1,
                title="Tokyo Day",
                activities=[
                    Activity(
                        name="Ramen Alley",
                        type="food",
                        time_slot="Evening",
                        cost_usd=15.0,
                        duration_hours=1.0,
                        crowd_level="medium",
                        description="Good food."
                    )
                ]
            )
        ]
    )
    
    result = agent.calculate_budget(constraints, itinerary)
    
    assert len(result.budget_summary) == 2
    assert result.budget_summary[0].category == "accommodation"
    assert result.budget_summary[0].status == "Within"
    assert result.budget_summary[1].category == "food"
    assert result.budget_summary[1].status == "Exceeded"

def test_review_agent_mocked_pass():
    """Test ReviewAgent PASS validation with mocked API responses."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    expected_review = ReviewOutput(
        status="PASS",
        failure_reason=None,
        validation_checklist={
            "duration_fit": True,
            "city_coverage": True,
            "budget_compliance": True,
            "preference_alignment": True,
            "avoidance_compliance": True,
            "logistics_realism": True
        }
    )
    
    mock_response.parsed = expected_review
    mock_client.models.generate_content.return_value = mock_response
    
    agent = ReviewAgent(client=mock_client)
    
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=1,
        budget_usd=1000.0,
        preferences=["food"],
        avoidances=["crowds"]
    )
    itinerary = LogisticsOutput(days=[])
    budget = BudgetOutput(budget_summary=[])
    
    result = agent.validate_itinerary(constraints, itinerary, budget)
    
    assert result.status == "PASS"
    assert result.failure_reason is None
    assert result.validation_checklist.budget_compliance is True

def test_review_agent_mocked_fail():
    """Test ReviewAgent FAIL validation with mocked API responses."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    expected_review = ReviewOutput(
        status="FAIL",
        failure_reason="Total estimated cost ($3,500) exceeds budget limit ($3,000)",
        validation_checklist={
            "duration_fit": True,
            "city_coverage": True,
            "budget_compliance": False,
            "preference_alignment": True,
            "avoidance_compliance": True,
            "logistics_realism": True
        }
    )
    
    mock_response.parsed = expected_review
    mock_client.models.generate_content.return_value = mock_response
    
    agent = ReviewAgent(client=mock_client)
    
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=1,
        budget_usd=3000.0,
        preferences=["food"],
        avoidances=["crowds"]
    )
    itinerary = LogisticsOutput(days=[])
    budget = BudgetOutput(budget_summary=[])
    
    result = agent.validate_itinerary(constraints, itinerary, budget)
    
    assert result.status == "FAIL"
    assert "exceeds budget limit" in result.failure_reason
    assert result.validation_checklist.budget_compliance is False

@pytest.mark.skipif(not API_KEY_PRESENT, reason="GEMINI_API_KEY not found in environment")
def test_budget_review_live_flow():
    """Live integration test for Budget & Review agents, executing only if API key is present."""
    budget_agent = BudgetAgent()
    review_agent = ReviewAgent()
    
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=2,
        budget_usd=800.0,
        preferences=["food"],
        avoidances=["crowds"]
    )
    itinerary = LogisticsOutput(
        days=[
            DayItinerary(
                day_number=1,
                title="Tokyo Day 1",
                activities=[
                    Activity(
                        name="Koenji Ramen Alley",
                        type="food",
                        time_slot="Evening",
                        cost_usd=12.0,
                        duration_hours=1.5,
                        crowd_level="low",
                        description="Quiet ramen spot"
                    )
                ],
                transit_info="Walk"
            ),
            DayItinerary(
                day_number=2,
                title="Tokyo Day 2",
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
                transit_info="Train"
            )
        ]
    )
    
    budget_result = budget_agent.calculate_budget(constraints, itinerary)
    assert len(budget_result.budget_summary) > 0
    
    review_result = review_agent.validate_itinerary(constraints, itinerary, budget_result)
    assert review_result.status in ["PASS", "FAIL"]
    assert hasattr(review_result.validation_checklist, "budget_compliance")
