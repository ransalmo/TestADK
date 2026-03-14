import vertexai
from vertexai.preview import reasoning_engines
from google.oauth2 import service_account


class VertexAIAgentFactory:
    def __init__(self, project: str, location: str = "us-central1", key_path: str = None):
        """
        Initializes the connection to your GCP project using an optional Service Account.

        Args:
            project: The GCP Project ID.
            location: The GCP region (e.g., 'us-central1').
            key_path: Path to the service_account_key.json file.
        """
        self.project = project
        self.location = location
        self.credentials = None

        if key_path:
            # Load credentials from the specific JSON file
            self.credentials = service_account.Credentials.from_service_account_file(key_path)
            print(f"Authenticated using service account: {key_path}")

        # Initialize Vertex AI with the specific credentials
        vertexai.init(
            project=self.project,
            location=self.location,
            credentials=self.credentials
        )

    def get_remote_agent(self, resource_id: str):
        """
        Retrieves a deployed agent by its Resource ID.
        """
        try:
            # The ReasoningEngine class will now use the credentials from vertexai.init()
            remote_agent = reasoning_engines.ReasoningEngine(resource_id)
            return remote_agent
        except Exception as e:
            print(f"Error retrieving remote agent: {e}")
            return None


