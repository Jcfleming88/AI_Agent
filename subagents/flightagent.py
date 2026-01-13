# System imports
import os
import re
import random
from datetime import datetime, timedelta

# LLM components
from tools.colour_tools import *
from tools.web_tools import *
from responses.response import *
from models.models import *
from context.context import *
from states.states import *

# Utility functions
from utils.dictutils import *
from utils.fileutils import *
from utils.strutils import *

# External libraries
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.messages import AIMessage


flight_agent = create_agent(
    model=llm_basic,
    system_prompt=f"You are a sub agent that focuses only on finding flights to different destinations. When asked to find flights, you should search the web using the specified bits of information and return a list of flights that match the parameters set out.",
    tools=[web_search],
    context_schema=Context,
    response_format=ToolStrategy(FlightResponse)
)

@tool
def search_for_flights(
    destination: str,
    departure_city: str,
    travel_date: datetime,
    number_of_nights: int,
    number_of_adults: int,
    number_of_children: Optional[int],
    budget: Optional[float],
    max_number_of_changes: Optional[int],
    runtime: ToolRuntime
    ) -> list[FlightInfo] | str:
    """Get a list of flights to and from a destination."""

    if destination is None or destination == "":
        return "No destination has been provided for the flights."

    if departure_city is None or departure_city == "":
        return "No departure city has been given."

    if travel_date is None:
        return "No travel date has been specified."
    if travel_date.date() < datetime.today().date():
        return "The travel date has already passed. A date after todays date should be provided."

    return_date = travel_date + timedelta(days=number_of_nights)

    formatted_message = f"Search for flights to {destination} from {departure_city}. The flights should leave {travel_date.strftime('%d-%m-%Y')} and return on {return_date.strftime('%d-%m-%Y')}. The flights should be for {number_of_adults} adults"
    
    if number_of_children:
        formatted_message += f" and {number_of_adults} children"

    if budget:
        formatted_message += f". There is a maximum budget of {budget} for the flights"

    if max_number_of_changes is not None: 
        formatted_message += f". The flights shouldn't have a maximum number of changes of {max_number_of_changes} and if zero then all flights should be direct"

    formatted_message += f". Return a list of flights that match the criteria above."
    formatted_message = formatted_message.strip()

    print(ToolMessage(content=formatted_message, tool_call_id=runtime.tool_call_id))

    config = RunnableConfig(configurable={"thread_id": "1"})

    response = flight_agent.invoke(
        { "messages": [AIMessage(content=formatted_message)] },
        context=Context(user_id="1"),
        config=config
    )

    return response["messages"][-1].content

flight_tools = [obj for obj in globals().values() if isinstance(obj, BaseTool)]