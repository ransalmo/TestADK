from abc import ABC, abstractmethod

class IOrchestrator(ABC):
    """
    An interface for an orchestrator that runs a user's input.
    """

    @abstractmethod
    def run(self, user_input: str) -> str:
        """
        Runs the orchestrator with the given user input.

        Args:
            user_input: The input from the user.

        Returns:
            The response from the orchestrator.
        """
        pass
