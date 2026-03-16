from google.adk.models import Gemini
from google.adk.agents import Agent
import logging
from src.agent_rest_api.agent.iorchestator import IOrchestrator

logger = logging.getLogger(__name__)


class GeminiOrchestrator(IOrchestrator):
    def __init__(self, model_name: str, project_id: str, location: str, agents: list[Agent]):
        logger.info("Initializing GeminiOrchestrator")

        self.model_name = model_name
        self.project_id = project_id
        self.location = location
        self.agents = agents

        self.__init_llm()
        self.__init_router()

        logger.info("GeminiOrchestrator initialized")

    def __init_llm(self):

        logger.info("Initializing LLM")

        self.llm = Gemini(
            model=self.model_name,
            project=self.project_id,
            location=self.location,
        )

    def __init_router(self):

        logger.info("Initializing router agent")

        instruction = """
        You are an orchestration agent.

        Your job is to decide which specialized agent should handle the request.

        Rules:
        - Select the best agent based on the task
        - Use only one agent unless multiple are required
        - Always return the final answer to the user
        """

        self.router = Agent(
            name="orchestrator",
            model=self.llm,
            instruction=instruction,
            tools=self.agents   # sub-agents exposed as tools
        )

    def run(self, user_input: str):
        logger.info(f"User input: {user_input}")
        response = self.router.run(user_input)
        logger.info(f"Response: {response}")
        return response
