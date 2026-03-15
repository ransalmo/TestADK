from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Represents the application settings.
    """
    log_level: str = "DEBUG"
    model_name: str = ""
    model_url: str = ""
    model_key: str = ""
    agent_repository: str = "json_file"
    db_user: str = ""
    db_name: str = ""
    project_id: str = ""
    location: str = ""

