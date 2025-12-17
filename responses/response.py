from dataclasses import dataclass

# We use a dataclass here, but Pydantic models are also supported.
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A response (always required)
    response: str
    # Coding languages used (optional)
    languages: list[str] | None = None