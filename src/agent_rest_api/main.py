import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.agent_rest_api.entities.settings import Settings
from src.agent_rest_api.service.service_logic import ServiceLogic
from src.agent_rest_api.views.router.v1 import chat, health

# Initialize settings
settings = Settings()

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Include routers
app.include_router(chat.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")

# Create ServiceLogic instance
service_logic = ServiceLogic(settings)
app.state.service_logic = service_logic

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to catch and log all exceptions.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
