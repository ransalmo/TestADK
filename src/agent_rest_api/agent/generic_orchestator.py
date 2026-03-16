from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
import logging

logger = logging.getLogger(__name__)


class GenericOrchestrator:
    def __init__(self, model_name: str, key: str, model_url: str, agents: list[Agent]):
        logger.info("Initializing Orchestrator")

        self.model_name = model_name
        self.key = key
        self.model_url = model_url
        self.agents = agents

        self.__init_llm()
        self.__init_router()

        logger.info("Orchestrator initialized")

    def __init_llm(self):

        logger.info("Initializing LLM")

        self.llm = LiteLlm(
            model=f"openai/{self.model_name}",
            api_key=self.key,
            api_base=self.model_url
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