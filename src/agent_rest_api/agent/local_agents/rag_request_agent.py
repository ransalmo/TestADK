import logging
import requests
from google.adk.agents import Agent
from google.adk.tools import tool

logger = logging.getLogger(__name__)

class RagRequestAgent(Agent):
    """
    An agent that retrieves information about project status, metrics, and UDF documents
    by making a request to a web service.
    """

    def __init__(self, web_service_url: str):
        """
        Initializes the RagRequestAgent.

        Args:
            web_service_url: The base URL of the web service to query.
        """
        super().__init__(
            name="rag_request_agent",
            description="Retrieves project status, project metrics, and information about a document called UDF.",
            tools=[self.retrieve_information]
        )
        self.web_service_url = web_service_url

    @tool
    def retrieve_information(self, query: str) -> str:
        """
        Makes a request to the web service to retrieve information.

        Args:
            query: The query to send to the web service.

        Returns:
            The response from the web service as a string.
        """
        endpoint = f"{self.web_service_url}/retrieve"
        logger.info(f"Making request to {endpoint} with query: {query}")
        try:
            response = requests.post(endpoint, json={"query": query})
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to make request to web service: {e}", exc_info=True)
            return f"Error: Could not retrieve information. {e}"

    def run(self, query: str) -> str:
        """
        The main entry point for the agent.
        """
        return self.retrieve_information(query=query)
