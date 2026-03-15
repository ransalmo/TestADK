import json
import logging
from typing import List, Optional
from cachetools import cached, TTLCache
from src.agent_rest_api.entities.agent_metadata import AgentMetadata
from src.agent_rest_api.repositories.agent_repository import AgentRepository

logger = logging.getLogger(__name__)

class AgentRepositoryJsonFile(AgentRepository):
    """
    An implementation of AgentRepository that reads agent metadata from a local JSON file.
    """

    def __init__(self, file_path: str, cache_ttl_seconds: int = 300):
        """
        Initializes the AgentRepositoryJsonFile.

        Args:
            file_path: The path to the local JSON file.
            cache_ttl_seconds: The time-to-live for the cache in seconds.
        """
        self.file_path = file_path
        self.cache = TTLCache(maxsize=1, ttl=cache_ttl_seconds)

    @cached(cache=lambda self: self.cache)
    def _get_all_agents(self) -> List[AgentMetadata]:
        """
        Reads the agent metadata from the local JSON file and caches it.
        """
        logger.info(f"Fetching agent metadata from {self.file_path}")
        try:
            with open(self.file_path, 'r') as f:
                data = f.read()
            agents_data = json.loads(data)
            return [AgentMetadata(**agent_data) for agent_data in agents_data]
        except FileNotFoundError:
            logger.error(f"Agent metadata file not found at {self.file_path}")
            return []
        except Exception as e:
            logger.error(f"Failed to fetch or parse agent metadata from file: {e}", exc_info=True)
            return []

    def find_by_friendly_name(self, friendly_name: str) -> Optional[AgentMetadata]:
        """
        Finds an agent by its friendly name from the cached data.
        """
        all_agents = self._get_all_agents()
        for agent in all_agents:
            if agent.agent == friendly_name:
                return agent
        return None

    def search(self, author: str, location: str) -> List[AgentMetadata]:
        """
        Searches for agents by author and location from the cached data.
        """
        all_agents = self._get_all_agents()
        results = []
        for agent in all_agents:
            if (not author or agent.author == author) and \
               (not location or agent.location == location):
                results.append(agent)
        return results
