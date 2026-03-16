from src.agent_rest_api.entities.settings import Settings
from src.agent_rest_api.repositories.agent_repository import AgentRepository
from src.agent_rest_api.repositories.agent_repository_database import AgentRepositoryDatabase
from src.agent_rest_api.repositories.agent_repository_json_file import AgentRepositoryJsonFile
from src.agent_rest_api.repositories.agent_repository_json_gcs import AgentRepositoryJsonGCS


class ServiceLogic:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.agents = []
        # just create the agent repository if we are using Vertex AI agents, since in that case we'll be fetching metadata from Vertex AI directly
        self.agent_repository = None if settings.use_vertex_ai_agents else self._create_agent_repository()
        if self.agent_repository:
            pass
        else:

            



    def _create_agent_repository(self) -> AgentRepository:
        """
        Creates an instance of an agent repository based on the settings.
        """
        match self.settings.agent_repository:
            case "database":
                return AgentRepositoryDatabase(
                    db_user=self.settings.db_user,
                    db_name=self.settings.db_name,
                    instance_connection_name=f"{self.settings.project_id}:{self.settings.location}:main-instance",
                )
            case "json_gcs":
                return AgentRepositoryJsonGCS(
                    bucket_name=self.settings.agent_metadata_bucket,
                    file_path="agents.json",
                )
            case "json_file":
                return AgentRepositoryJsonFile(file_path="agents.json")
            case _:
                raise ValueError(f"Unknown agent repository type: {self.settings.agent_repository}")

    def process_request(self, request_data):
        pass