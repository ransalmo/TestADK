import logging
from fastapi import APIRouter, Depends
from src.agent_rest_api.dependencies import get_service_logic
from src.agent_rest_api.entities.chat_request import ChatRequest
from src.agent_rest_api.service.service_logic import ServiceLogic

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat")
async def chat(
    chat_request: ChatRequest,
    service_logic: ServiceLogic = Depends(get_service_logic),
):
    """
    Receives a chat request and returns a response.
    """
    try:
        logger.info(f"Received chat request: {chat_request.message}")
        response = service_logic.process_request(chat_request)
        logger.info(f"Sending response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise
