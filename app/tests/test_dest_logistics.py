import os
import pytest
from unittest.mock import MagicMock
from app.agents.destination import DestinationResearchAgent
from app.agents.logistics import LogisticsAgent
from app.models import TravelConstraints, DestinationCuration, RecommendedPlace, LogisticsOutput, DayItinerary, Activity

# Check if GEMINI_API_KEY is configured in the environment
API_KEY_PRESENT = os.getenv("GEMINI_API_KEY") not in [None, "", "YOUR_GEMINI_API_KEY_HERE"]

def test_destination_research_mocked():
    """Test DestinationResearchAgent with mocked API responses."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    expected_curation = DestinationCuration(
        places=[
            RecommendedPlace(
                name="Nezu Shrine",
                type="temple",
                neighborhood="Yanaka",
                description="Quiet shrine with historical architecture.",
                crowd_level="low",
                estimated_cost_usd=5.0,
                estimated_duration_hours=1.5
            )
        ],
        stay_neighborhoods=["Yanaka"]
    )
    
    mock_response.parsed = expected_curation
    mock_client.models.generate_content.return_value = mock_response
    
    agent = DestinationResearchAgent(client=mock_client)
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=1,
        budget_usd=1000.0,
        preferences=["temples"],
        avoidances=["crowds"]
    )
    
    result = agent.curate_destination(constraints)
    
    assert len(result.places) == 1
    assert result.places[0].name == "Nezu Shrine"
    assert result.stay_neighborhoods == ["Yanaka"]

def test_logistics_agent_mocked():
    """Test LogisticsAgent with mocked API responses."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    expected_logistics = LogisticsOutput(
        days=[
            DayItinerary(
                day_number=1,
                title="Quiet Temples & Flavors",
                activities=[
                    Activity(
                        name="Nezu Shrine",
                        type="temple",
                        time_slot="Morning",
                        cost_usd=5.0,
                        duration_hours=1.5,
                        crowd_level="low",
                        description="Quiet shrine with historical architecture."
                    )
                ],
                transit_info="Walk (10 mins)"
            )
        ]
    )
    
    mock_response.parsed = expected_logistics
    mock_client.models.generate_content.return_value = mock_response
    
    agent = LogisticsAgent(client=mock_client)
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=1,
        budget_usd=1000.0,
        preferences=["temples"],
        avoidances=["crowds"]
    )
    curation = DestinationCuration(
        places=[
            RecommendedPlace(
                name="Nezu Shrine",
                type="temple",
                neighborhood="Yanaka",
                description="Quiet shrine.",
                crowd_level="low",
                estimated_cost_usd=5.0,
                estimated_duration_hours=1.5
            )
        ],
        stay_neighborhoods=["Yanaka"]
    )
    
    result = agent.sequence_itinerary(constraints, curation)
    
    assert len(result.days) == 1
    assert result.days[0].day_number == 1
    assert result.days[0].activities[0].name == "Nezu Shrine"
    assert result.days[0].activities[0].time_slot == "Morning"

@pytest.mark.skipif(not API_KEY_PRESENT, reason="GEMINI_API_KEY not found in environment")
def test_dest_logistics_live_flow():
    """Live integration test linking Destination & Logistics agents sequentially."""
    dest_agent = DestinationResearchAgent()
    log_agent = LogisticsAgent()
    
    constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo"],
        duration_days=3,
        budget_usd=1500.0,
        preferences=["food", "temples"],
        avoidances=["crowds"]
    )
    
    curation = dest_agent.curate_destination(constraints)
    assert len(curation.places) > 0
    assert len(curation.stay_neighborhoods) > 0
    
    itinerary = log_agent.sequence_itinerary(constraints, curation)
    assert len(itinerary.days) == 3
    for day in itinerary.days:
        assert len(day.activities) > 0
        assert day.title != ""
