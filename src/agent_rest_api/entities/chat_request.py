from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    """
    Represents a chat request entity.
    """
    message: str
    source: Optional[str] = None
    gen_model_to_use: Optional[str] = None
