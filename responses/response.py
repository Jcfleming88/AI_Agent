from pydantic import BaseModel, Field
from dataclasses import dataclass

@dataclass
class FlightInfo:
    airline: str = Field(..., description="The airline operating the flight.")
    flight_number: str = Field(..., description="The flight number.")
    departure_city: str = Field(..., description="The city from which the flight departs.")
    arrival_city: str = Field(..., description="The city where the flight arrives.")
    departure_time: str = Field(..., description="The departure data and time of the flight in the format HH:mm dd-MM-yyyy.")
    arrival_time: str = Field(..., description="The arrival date and time of the flight in the format HH:mm dd-MM-yyyy.")
    price: float = Field(..., description="The price of the flight.")
    number_of_changes: int = Field(..., description="The total number of stop-offs/changes for the flight.")
    stop_offs: list[str] = Field(..., description="A list of stop-off cities for the flight.")
    total_flight_time: str = Field(..., description="The total flight time from departure to destination.")
    
@dataclass
class FlightResponse:
    """Flight response schema. Includes a list of flight options."""
    response: str

    outbound_flights: list[FlightInfo] = Field(default=[], description="A list of outbound flight options, each option is a list of FlightInfo objects representing the flight.")
    inbound_flights: list[FlightInfo] = Field(default=[], description="A list of inbound flight options, each option is a list of FlightInfo objects representing the flight.")

@dataclass
class Hotel:
    name: str = Field(..., description="The name of the hotel.")
    location: str = Field(..., description="The location of the hotel.")
    star_rating: int = Field(..., description="The star rating of the hotel.")
    price_per_night: float = Field(..., description="The price per night for the lowest price hotel room at matches the search parameters.")
    amenities: list[str] = Field(..., description="A list of amenities provided by the hotel.")

@dataclass
class HotelResponse:
    """Hotel response schema. Includes a list of hotel options."""
    response: str

    hotels: list[Hotel] = Field(default=[], description="A list of hotel options.")

@dataclass
class Activity:
    name: str = Field(..., description="The name of the activity.")
    description: str = Field(..., description="A brief description of the activity.")
    price: float = Field(..., description="The price of the activity.")
    duration: str = Field(..., description="The duration of the activity.")

@dataclass
class ActivityResponse:
    """Activity response schema. Includes a list of activity options."""
    response: str

    activities: list[Activity] = Field(default=[], description="A list of activity options.")

@dataclass
class Attraction:
    name: str = Field(..., description="The name of the attraction.")
    description: str = Field(..., description="A brief description of the attraction.")
    location: str = Field(..., description="The location of the attraction.")
    opening_hours: str = Field(..., description="The opening hours of the attraction.")
    price: float = Field(..., description="The price of admission to the attraction.")

@dataclass
class AttractionResponse:
    """Attraction response schema. Includes a list of attraction options."""
    response: str

    attractions: list[Attraction] = Field(default=[], description="A list of attraction options.")

@dataclass
class MainResponse:
    """Response schema for the main agent. Includes optional fields for different types of returned information."""
    # A response (always required)
    response: str

    # Returned info (optional)
    flights: list[list[FlightInfo]] = Field(default=[], description="A list of flight options, each option is a list of FlightInfo objects representing the legs of the flight.")
    hotels: list[Hotel] = Field(default=[], description="A list of hotel options.")
    activities: list[Activity] = Field(default=[], description="A list of activity options.")
    attractions: list[Attraction] = Field(default=[], description="A list of attraction options.")