from src.agent_rest_api.entities.settings import Settings

class ServiceLogic:
    def __init__(self, settings: Settings):
        self.settings = settings

    def process_request(self, request_data):
        pass