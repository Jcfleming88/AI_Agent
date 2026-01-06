import os
from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    return tavily_client.search(query=query)