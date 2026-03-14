from abc import ABC, abstractmethod
from typing import List, Optional
from src.agent_rest_api.entities.agent_metadata import AgentMetadata

class AgentRepository(ABC):
    """
    An interface for a repository that stores and retrieves agent metadata.
    """

    @abstractmethod
    def find_by_friendly_name(self, friendly_name: str) -> Optional[AgentMetadata]:
        """
        Finds an agent by its friendly name.

        Args:
            friendly_name: The friendly name of the agent to find.

        Returns:
            The agent metadata if found, otherwise None.
        """
        pass

    @abstractmethod
    def search(self, author: str, location: str) -> List[AgentMetadata]:
        """
        Searches for agents by author and location.

        Args:
            author: The author of the agents to find.
            location: The location of the agents to find.

        Returns:
            A list of agent metadata matching the search criteria.
        """
        pass
