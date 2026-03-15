from fastapi import APIRouter, Depends
from src.agent_rest_api.dependencies import get_service_logic
from src.agent_rest_api.entities.chat_request import ChatRequest
from src.agent_rest_api.service.service_logic import ServiceLogic

router = APIRouter()

@router.post("/chat")
async def chat(
    chat_request: ChatRequest,
    service_logic: ServiceLogic = Depends(get_service_logic),
):
    """
    Receives a chat request and returns a response.
    """
    return service_logic.process_request(chat_request)
