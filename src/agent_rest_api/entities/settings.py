from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Represents the application settings.
    """
    log_level: str = "DEBUG"
    model_name: str = ""
    model_url: str = ""
    model_key: str = ""
