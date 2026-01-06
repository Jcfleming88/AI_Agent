from dataclasses import dataclass

# We use a dataclass here, but Pydantic models are also supported.
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A response (always required)
    response: str

    # Recipe info (optional)
    ingredients: list[str] | None = None
    steps: list[str] | None = None
    url: str | None = None