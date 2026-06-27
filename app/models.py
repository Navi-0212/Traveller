from pydantic import BaseModel, Field
from typing import List, Optional

class Activity(BaseModel):
    name: str = Field(..., description="Name of the activity, restaurant, temple, or sightseeing spot")
    type: str = Field(..., description="Category of activity: 'food', 'sightseeing', 'temple', 'transit', 'accommodation'")
    time_slot: str = Field(..., description="Time block for the activity: 'Morning', 'Afternoon', 'Evening'")
    cost_usd: float = Field(..., description="Estimated cost of this activity in USD")
    duration_hours: float = Field(..., description="Estimated duration in hours")
    crowd_level: str = Field(..., description="Expected crowd density: 'low', 'medium', 'high'")
    description: str = Field(..., description="Short explanation of what to do, alignment with preferences, or tips")

class DayItinerary(BaseModel):
    day_number: int = Field(..., description="Sequential day number, starting at 1")
    title: str = Field(..., description="Summary theme of the day (e.g. 'Quiet Temples & Local Flavors')")
    activities: List[Activity] = Field(..., description="List of activities planned for this day")
    transit_info: Optional[str] = Field(None, description="Overview of local transit used during the day")

class BudgetBreakdown(BaseModel):
    category: str = Field(..., description="Category of spend: 'flights', 'accommodation', 'transit', 'food', 'activities', 'buffer'")
    allocated_usd: float = Field(..., description="Target or allocated budget in USD")
    estimated_cost_usd: float = Field(..., description="Estimated cost in USD computed by the Budget Agent")
    status: str = Field(..., description="Budget status: 'Within' or 'Exceeded'")

class RecommendedPlace(BaseModel):
    name: str = Field(..., description="Name of the attraction, temple, scenic spot, or restaurant")
    type: str = Field(..., description="Category: 'food', 'sightseeing', 'temple'")
    neighborhood: str = Field(..., description="Area or neighborhood (e.g. 'Yanaka', 'Arashiyama', 'Shimokitazawa')")
    description: str = Field(..., description="Description, why it matches user vibes, and tips")
    crowd_level: str = Field(..., description="Expected crowd level: 'low', 'medium', 'high'")
    estimated_cost_usd: float = Field(..., description="Approximate entry fee or meal cost per person in USD")
    estimated_duration_hours: float = Field(..., description="Average time spent visiting in hours")

class DestinationCuration(BaseModel):
    places: List[RecommendedPlace] = Field(..., description="List of recommended places matching constraints")
    stay_neighborhoods: List[str] = Field(..., description="Recommended neighborhoods to stay in each city")

class LogisticsOutput(BaseModel):
    days: List[DayItinerary] = Field(..., description="Day-by-day organized itineraries")

class BudgetOutput(BaseModel):
    budget_summary: List[BudgetBreakdown] = Field(..., description="List of budget category breakdowns")

class ValidationChecklist(BaseModel):
    duration_fit: bool = Field(True, description="True if the itinerary has exactly the duration specified in constraints.")
    city_coverage: bool = Field(True, description="True if all requested cities are represented in the day-by-day plan.")
    budget_compliance: bool = Field(True, description="True if total estimated costs are within the budget limit.")
    preference_alignment: bool = Field(True, description="True if activities align with the user's positive preferences.")
    avoidance_compliance: bool = Field(True, description="True if recommendations respect user avoidances.")
    logistics_realism: bool = Field(True, description="True if active hours and geographical sequencing are realistic.")

class ReviewOutput(BaseModel):
    status: str = Field(..., description="'PASS' or 'FAIL'")
    failure_reason: Optional[str] = Field(None, description="Detailed explanation of failure if status is FAIL, otherwise null")
    validation_checklist: ValidationChecklist = Field(..., description="Checklist of pass/fail criteria")

class TravelConstraints(BaseModel):
    destination: str = Field(..., description="Target country or main region")
    cities: List[str] = Field(..., description="List of specific cities to visit")
    duration_days: int = Field(..., description="Total length of the trip in days")
    budget_usd: float = Field(..., description="Maximum budget in USD")
    preferences: List[str] = Field(..., description="User interests (e.g., temples, food, shopping, nature)")
    avoidances: List[str] = Field(..., description="User avoidances (e.g., crowds, tourist traps, long walks)")
    travel_style: str = Field("independent", description="Travel style: 'independent', 'guided group', etc.")
    accommodation_preference: str = Field("mid-range", description="Accommodation tier: 'budget', 'mid-range', 'luxury'")

class ItineraryPlan(BaseModel):
    destination: str = Field(..., description="Main destination")
    duration_days: int = Field(..., description="Duration of the trip in days")
    days: List[DayItinerary] = Field(..., description="Day-by-day itineraries")
    budget_summary: List[BudgetBreakdown] = Field(..., description="Category budget details")
    validation_passed: bool = Field(..., description="True if the plan successfully passed Review Agent checks")
    validation_notes: Optional[str] = Field(None, description="Reasoning or notes from the Review Agent gate")
