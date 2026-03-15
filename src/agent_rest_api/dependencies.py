from fastapi import Request
from src.agent_rest_api.service.service_logic import ServiceLogic

def get_service_logic(request: Request) -> ServiceLogic:
    return request.app.state.service_logic
