# System references
from typing import Optional
from datetime import datetime

# LLM references
from responses.response import *

# External references
from langchain.agents import AgentState
from langchain.tools import tool, BaseTool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage

class MainState(AgentState):
    """
    Custom state schema for the main agent.
    """
    
    # Travel details
    # Where the user wants to travel
    destination: str
    # The data of travel
    travel_date: datetime
    # The number of nights stay
    number_of_nights: int
    # The number of adults travelling
    number_of_adults: int
    # The number of children travelling. This is optional as children are not always travelling and must be with an adult
    number_of_children: Optional[int]

    # Flight details
    # The city you want to depart from
    departure_city: str
    # The maximum price for the flights
    flight_budget: Optional[float]
    # The maximum number of changes to get to the destination
    max_number_of_changes: Optional[int]

    # Accommodation details
    # The type of accomodation the user is looking for
    accommodation_type: Optional[str]
    # The minimum star rating of the accomodation
    star_rating: Optional[int]
    # A list of the amenities at the accomodation
    amenities: list[str]

    # Activity preferences
    # A list of interests for the user
    interests: list[str]
    # The maximum price of an activity per person
    activity_budget: Optional[float]

    # Selected info
    # The flights the user has accepted
    selected_flight: list[FlightInfo] | None
    # The hotel the user has selected
    selected_hotel: Hotel | None 
    # The activities the user wants to do
    selected_activities: list[Activity]
    # The attractions the user wants to attend
    selected_attractions: list[Attraction]

@tool
def get_destination(runtime: ToolRuntime) -> str:
    """Get the destination that the user wants to go to."""
    try:
        return runtime.state["destination"]
    except:
        return "No destination found in state."

@tool
def set_destination(dest: str, runtime: ToolRuntime) -> Command:
    """Set the destination that the user wants to go to."""
    return Command(update={
        "destination": dest,
        "messages": [ToolMessage(f"Updated destination to {dest}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_travel_date(runtime: ToolRuntime) -> datetime | str:
    """Get the travel date."""
    try:
        return runtime.state["travel_date"]
    except:
        return "No travel date found in state."

@tool
def set_travel_date(date: datetime, runtime: ToolRuntime) -> Command:
    """Sets the date at which the user wants to travel."""
    return Command(update={
        "travel_date": date,
        "messages": [ToolMessage(f"Updated travel date to {date}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_number_of_nights(runtime: ToolRuntime) -> int | str:
    """Get the number of nights for the stay."""
    try:
        return runtime.state["number_of_nights"]
    except:
        return "No number of nights found in state."

@tool
def set_number_of_nights(nights: int, runtime: ToolRuntime) -> Command:
    """Sets the number of nights the user wants to stay."""
    return Command(update={
        "number_of_nights": nights,
        "messages": [ToolMessage(f"Updated number of nights to {nights}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_number_of_adults(runtime: ToolRuntime) -> int | str:
    """Get the number of adults travelling."""
    try:
        return runtime.state["number_of_adults"]
    except:
        return "No number of adults found in state."

@tool
def set_number_of_adults(adults: int, runtime: ToolRuntime) -> Command:
    """Sets the number of adults going on holiday"""
    return Command(update={
        "number_of_adults": adults,
        "messages": [ToolMessage(f"Updated number of adults to {adults}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_number_of_children(runtime: ToolRuntime) -> Optional[int]:
    """Get the number of children travelling."""
    try:
        return runtime.state["number_of_children"]
    except:
        return 0

@tool
def set_number_of_children(children: int, runtime: ToolRuntime) -> Command:
    """Sets the number of children that are coming on the holiday."""
    return Command(update={
        "number_of_children": children,
        "messages": [ToolMessage(f"Updated number of children to {children}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_departure_city(runtime: ToolRuntime) -> str:
    """Get the departure city."""
    try:
        return runtime.state["departure_city"]
    except:
        return "No departure city found in state."

@tool
def set_departure_city(city: str, runtime: ToolRuntime) -> Command:
    """Sets the city the user wants to depart from."""
    return Command(update={
        "departure_city": city,
        "messages": [ToolMessage(f"Updated departure city to {city}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_budget(runtime: ToolRuntime) -> Optional[float]:
    """Get the flight budget."""
    try:
        return runtime.state["flight_budget"]
    except:
        return None

@tool
def set_budget(amount: float, runtime: ToolRuntime) -> Command:
    """Sets the maximum budget for the flights"""
    return Command(update={
        "flight_budget": amount,
        "messages": [ToolMessage(f"Updated budget to {amount}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_max_number_of_changes(runtime: ToolRuntime) -> Optional[int]:
    """Get the maximum number of flight changes."""
    try:
        return runtime.state["max_number_of_changes"]
    except:
        return None

@tool
def set_max_number_of_changes(changes: int, runtime: ToolRuntime) -> Command:
    """Sets the maximum number of changes for a flight"""
    return Command(update={
        "max_number_of_changes": changes,
        "messages": [ToolMessage(f"Updated max number of changes to {changes}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_accommodation_type(runtime: ToolRuntime) -> Optional[str]:
    """Get the accommodation type."""
    try:
        return runtime.state["accommodation_type"]
    except:
        return None

@tool
def set_accommodation_type(acc_type: str, runtime: ToolRuntime) -> Command:
    """Sets the type of accomodation the user wants to search for."""
    return Command(update={
        "accommodation_type": acc_type,
        "messages": [ToolMessage(f"Updated accommodation type to {acc_type}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_star_rating(runtime: ToolRuntime) -> Optional[int]:
    """Get the minimum star rating for accommodation."""
    try:
        return runtime.state["star_rating"]
    except:
        return None

@tool
def set_star_rating(rating: int, runtime: ToolRuntime) -> Command:
    """Sets the minimum star rating of any accomodation"""
    return Command(update={
        "star_rating": rating,
        "messages": [ToolMessage(f"Updated star rating to {rating}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_activity_budget(runtime: ToolRuntime) -> Optional[float]:
    """Get the activity budget per person."""
    try:
        return runtime.state["activity_budget"]
    except:
        return None
@tool
def set_activity_budget(amount: Optional[float], runtime: ToolRuntime) -> Command:
    """Sets the budget for activities. This is the most the user wants to spend on activities per person."""
    return Command(update={
        "activity_budget": amount,
        "messages": [ToolMessage(f"Updated activity budget to {amount}", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_selected_flight(runtime: ToolRuntime) -> list[FlightInfo] | str:
    """Get the selected flight."""
    try:
        return runtime.state["selected_flight"]
    except:
        return "No selected flight found in state."

@tool
def set_selected_flight(flight: list[FlightInfo] | None, runtime: ToolRuntime) -> Command:
    """Set the flights by which the user wants to travel to the destination."""
    return Command(update={
        "selected_flight": flight,
        "messages": [ToolMessage(f"Updated selected flight", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_selected_hotel(runtime: ToolRuntime) -> Hotel | str:
    """Get the selected hotel."""
    try:
        return runtime.state["selected_hotel"]
    except:
        return "No selected hotel found in state."

@tool
def set_selected_hotel(hotel: Hotel | None, runtime: ToolRuntime) -> Command:
    """Sets the hotel the user has selected. This is where they want to stay."""
    return Command(update={
        "selected_hotel": hotel,
        "messages": [ToolMessage(f"Updated selected hotel", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_amenities(runtime: ToolRuntime) -> list[str]:
    """Gets a list of amenities the user is looking for"""
    try:
        return runtime.state["amenities"]
    except:
        return []

@tool
def add_amenity(amenity: str, runtime: ToolRuntime) -> Command:
    """Adds a new amenity to the list"""
    amenities = runtime.state.get("amenities", [])
    return Command(update={
        "amenities": amenities + [amenity],
        "messages": [ToolMessage(f"{amenity} added to the amenities list.", tool_call_id=runtime.tool_call_id)]
    })

@tool
def remove_amenity(amenity: str, runtime: ToolRuntime) -> Command:
    """Removes an amenity from the list"""
    amenities = runtime.state.get("amenities", [])
    return Command(update={
        "amenities": [item for item in amenities if item != amenity],
        "messages": [ToolMessage(f"Removed {amenity} from list of amenities", tool_call_id=runtime.tool_call_id)]
    })

@tool
def clear_amenities(runtime: ToolRuntime) -> Command:
    """Clears all items in the amenities list"""
    return Command(update={
        "amenities": [],
        "messages": [ToolMessage("List of amenities cleared", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_interests(runtime: ToolRuntime) -> list[str]:
    """Gets a list of interests the user has"""
    try:
        return runtime.state["interests"]
    except:
        return []

@tool
def add_interest(interest: str, runtime: ToolRuntime) -> Command:
    """Adds a new interest to the list"""
    interests = runtime.state.get("interests", [])
    return Command(update={
        "interests": interests + [interest],
        "messages": [ToolMessage(f"{interest} added to the interests list.", tool_call_id=runtime.tool_call_id)]
    })

@tool
def remove_interest(interest: str, runtime: ToolRuntime) -> Command:
    """Removes an interest from the list"""
    interests = runtime.state.get("interests", [])
    return Command(update={
        "interests": [item for item in interests if item != interest],
        "messages": [ToolMessage(f"Removed {interest} from list of interests", tool_call_id=runtime.tool_call_id)]
    })

@tool
def clear_interests(runtime: ToolRuntime) -> Command:
    """Clears all items in the interests list"""
    return Command(update={
        "interests": [],
        "messages": [ToolMessage("List of interests cleared", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_selected_activities(runtime: ToolRuntime) -> list[Activity]:
    """Gets the list of selected activities"""
    try:
        return runtime.state["selected_activities"]
    except:
        return []

@tool
def add_selected_activity(activity: Activity, runtime: ToolRuntime) -> Command:
    """Adds an activity to the selected activities list"""
    activities = runtime.state.get("selected_activities", [])
    return Command(update={
        "selected_activities": activities + [activity],
        "messages": [ToolMessage("Activity added to selected activities.", tool_call_id=runtime.tool_call_id)]
    })

@tool
def remove_selected_activity(activity: Activity, runtime: ToolRuntime) -> Command:
    """Removes an activity from the selected activities list"""
    activities = runtime.state.get("selected_activities", [])
    return Command(update={
        "selected_activities": [item for item in activities if item != activity],
        "messages": [ToolMessage("Activity removed from selected activities", tool_call_id=runtime.tool_call_id)]
    })

@tool
def clear_selected_activities(runtime: ToolRuntime) -> Command:
    """Clears all selected activities"""
    return Command(update={
        "selected_activities": [],
        "messages": [ToolMessage("List of selected activities cleared", tool_call_id=runtime.tool_call_id)]
    })

@tool
def get_selected_attractions(runtime: ToolRuntime) -> list[Attraction]:
    """Gets the list of selected attractions"""
    try:
        return runtime.state["selected_attractions"]
    except:
        return []

@tool
def add_selected_attraction(attraction: Attraction, runtime: ToolRuntime) -> Command:
    """Adds an attraction to the selected attractions list"""
    attractions = runtime.state.get("selected_attractions", [])
    return Command(update={
        "selected_attractions": attractions + [attraction],
        "messages": [ToolMessage("Attraction added to selected attractions.", tool_call_id=runtime.tool_call_id)]
    })

@tool
def remove_selected_attraction(attraction: Attraction, runtime: ToolRuntime) -> Command:
    """Removes an attraction from the selected attractions list"""
    attractions = runtime.state.get("selected_attractions", [])
    return Command(update={
        "selected_attractions": [item for item in attractions if item != attraction],
        "messages": [ToolMessage("Attraction removed from selected attractions", tool_call_id=runtime.tool_call_id)]
    })

@tool
def clear_selected_attractions(runtime: ToolRuntime) -> Command:
    """Clears all selected attractions"""
    return Command(update={
        "selected_attractions": [],
        "messages": [ToolMessage("List of selected attractions cleared", tool_call_id=runtime.tool_call_id)]
    })

# Get a list of all tools
state_tools = [obj for obj in globals().values() if isinstance(obj, BaseTool)]