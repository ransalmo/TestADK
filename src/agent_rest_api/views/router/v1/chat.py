from fastapi import APIRouter
from src.agent_rest_api.entities.chat_request import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    """
    Receives a chat request and returns a response.
    """
    return {"message": "dummy response"}
