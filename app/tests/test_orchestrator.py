import os
import pytest
from unittest.mock import MagicMock
from app.agents.orchestrator import OrchestratorAgent
from app.models import TravelConstraints

# Check if GEMINI_API_KEY is configured in the environment
API_KEY_PRESENT = os.getenv("GEMINI_API_KEY") not in [None, "", "YOUR_GEMINI_API_KEY_HERE"]

def test_extract_constraints_mocked():
    """Test with mocked Gemini API client response to verify mapping logic."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    
    expected_constraints = TravelConstraints(
        destination="Japan",
        cities=["Tokyo", "Kyoto"],
        duration_days=5,
        budget_usd=3000.0,
        preferences=["food", "temples", "quiet experiences"],
        avoidances=["crowds", "tourist traps"],
        travel_style="independent",
        accommodation_preference="mid-range"
    )
    
    # Simulate both SDK parsed response object and text response fallback
    mock_response.parsed = expected_constraints
    mock_response.text = '{"destination": "Japan", "cities": ["Tokyo", "Kyoto"], "duration_days": 5, "budget_usd": 3000.0, "preferences": ["food", "temples", "quiet experiences"], "avoidances": ["crowds", "tourist traps"], "travel_style": "independent", "accommodation_preference": "mid-range"}'
    mock_client.models.generate_content.return_value = mock_response
    
    agent = OrchestratorAgent(client=mock_client)
    prompt = "Plan a 5-day trip to Japan. Tokyo + Kyoto. $3,000 budget. Love food and temples, hate crowds."
    result = agent.extract_constraints(prompt)
    
    assert result.destination == "Japan"
    assert "Tokyo" in result.cities
    assert "Kyoto" in result.cities
    assert result.duration_days == 5
    assert result.budget_usd == 3000.0
    assert "crowds" in result.avoidances
    assert "tourist traps" in result.avoidances

@pytest.mark.skipif(not API_KEY_PRESENT, reason="GEMINI_API_KEY not found in environment")
def test_extract_constraints_live_japan():
    """Live integration test for a Japan prompt, runs only if API key is present."""
    agent = OrchestratorAgent()
    prompt = "Plan a 5-day trip to Japan. Tokyo + Kyoto. $3,000 budget. Love food and temples, hate crowds."
    result = agent.extract_constraints(prompt)
    
    assert "japan" in result.destination.lower()
    assert any("tokyo" in c.lower() for c in result.cities)
    assert result.duration_days == 5
    assert result.budget_usd == 3000.0
    assert any("crowd" in a.lower() for a in result.avoidances)

@pytest.mark.skipif(not API_KEY_PRESENT, reason="GEMINI_API_KEY not found in environment")
def test_extract_constraints_live_italy():
    """Live integration test for an Italy prompt, runs only if API key is present."""
    agent = OrchestratorAgent()
    prompt = "10 days in Italy: Rome, Florence, Venice. $5000 budget. Interested in art, history and wine. Avoid long bus rides."
    result = agent.extract_constraints(prompt)
    
    assert "italy" in result.destination.lower()
    assert any("rome" in c.lower() for c in result.cities)
    assert result.duration_days == 10
    assert result.budget_usd == 5000.0
    assert any("art" in p.lower() for p in result.preferences)

@pytest.mark.skipif(not API_KEY_PRESENT, reason="GEMINI_API_KEY not found in environment")
def test_extract_constraints_live_weekend():
    """Live integration test for a spontaneous weekend prompt, runs only if API key is present."""
    agent = OrchestratorAgent()
    prompt = "Spontaneous 2-day beach getaway to Goa. Under $500. Just want relaxation, no museums."
    result = agent.extract_constraints(prompt)
    
    assert "goa" in result.destination.lower()
    assert result.duration_days == 2
    assert result.budget_usd <= 500.0
    assert any("museum" in a.lower() for a in result.avoidances)
