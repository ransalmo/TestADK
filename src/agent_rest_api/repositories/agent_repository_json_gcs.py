import json
import logging
from typing import List, Optional
from google.cloud import storage
from cachetools import cached, TTLCache
from src.agent_rest_api.entities.agent_metadata import AgentMetadata
from src.agent_rest_api.repositories.agent_repository import AgentRepository

logger = logging.getLogger(__name__)

class AgentRepositoryJsonGCS(AgentRepository):
    """
    An implementation of AgentRepository that reads agent metadata from a JSON file in a GCS bucket.
    """

    def __init__(self, bucket_name: str, file_path: str, service_account_path: Optional[str] = None, cache_ttl_seconds: int = 300):
        """
        Initializes the AgentRepositoryJson.

        Args:
            bucket_name: The name of the GCS bucket.
            file_path: The path to the JSON file in the bucket.
            service_account_path: The path to the service account file. If None, default credentials are used.
            cache_ttl_seconds: The time-to-live for the cache in seconds.
        """
        self.bucket_name = bucket_name
        self.file_path = file_path
        
        if service_account_path:
            self.storage_client = storage.Client.from_service_account_json(service_account_path)
        else:
            self.storage_client = storage.Client()

        self.cache = TTLCache(maxsize=1, ttl=cache_ttl_seconds)

    @cached(cache=lambda self: self.cache)
    def _get_all_agents(self) -> List[AgentMetadata]:
        """
        Downloads the agent metadata from GCS and caches it.
        """
        logger.info(f"Fetching agent metadata from gs://{self.bucket_name}/{self.file_path}")
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_path)
            data = blob.download_as_string()
            agents_data = json.loads(data)
            return [AgentMetadata(**agent_data) for agent_data in agents_data]
        except Exception as e:
            logger.error(f"Failed to fetch or parse agent metadata: {e}", exc_info=True)
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
