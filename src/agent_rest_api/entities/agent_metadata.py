from typing import Optional

from pydantic import BaseModel

class AgentMetadata(BaseModel):
    """
    Represents the metadata for an agent.
    """
    agent: str # The name of the agent.
    location: str = "us-central1" # The location of the agent.
    key_path: str # The path to the key file.
    description: Optional[str] # The description of the agent.
    author: Optional[str] # The author of the agent.
    friendly_name: str # A friendly name for the agent.
