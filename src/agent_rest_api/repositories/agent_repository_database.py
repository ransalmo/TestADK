import logging
from typing import List, Optional

from cachetools import TTLCache, cached
from google.cloud.sql.connector import Connector
from google.oauth2 import service_account
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from src.agent_rest_api.entities.agent_metadata import AgentMetadata
from src.agent_rest_api.repositories.agent_repository import AgentRepository

logger = logging.getLogger(__name__)


class AgentRepositoryDatabase(AgentRepository):
    """
    An implementation of AgentRepository that reads agent metadata from a
    Google Cloud SQL for PostgreSQL database.
    """

    def __init__(
        self,
        db_user: str,
        db_name: str,
        instance_connection_name: str,
        service_account_path: Optional[str] = None,
        cache_ttl_seconds: int = 300,
    ):
        """
        Initializes the AgentRepositoryDatabase.

        Args:
            db_user: The database user. For IAM authentication, this should be the service account email.
            db_name: The database name.
            instance_connection_name: The Cloud SQL instance connection name.
            service_account_path: The path to the service account file. If None, default credentials are used.
            cache_ttl_seconds: The time-to-live for the cache in seconds.
        """
        self.cache = TTLCache(maxsize=128, ttl=cache_ttl_seconds)
        
        if service_account_path:
            credentials = service_account.Credentials.from_service_account_file(service_account_path)
            self.connector = Connector(credentials=credentials)
        else:
            self.connector = Connector()

        def getconn():
            conn = self.connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                db=db_name,
                enable_iam_auth=True,
            )
            return conn

        self.engine = create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )
        self.Session = sessionmaker(bind=self.engine)

    def _execute_query(self, query: str, params: dict = None) -> List[dict]:
        """Executes a SQL query and returns the results."""
        try:
            with self.Session() as session:
                result = session.execute(text(query), params)
                return [row._asdict() for row in result]
        except Exception as e:
            logger.error(f"Database query failed: {e}", exc_info=True)
            return []

    @cached(cache=lambda self: self.cache)
    def find_by_friendly_name(self, friendly_name: str) -> Optional[AgentMetadata]:
        """Finds an agent by its friendly name from the database."""
        logger.info(f"Fetching agent '{friendly_name}' from database.")
        query = "SELECT * FROM agent_metadata WHERE agent = :friendly_name LIMIT 1"
        params = {"friendly_name": friendly_name}
        result = self._execute_query(query, params)
        if result:
            return AgentMetadata(**result[0])
        return None

    @cached(cache=lambda self: self.cache)
    def search(self, author: Optional[str] = None, location: Optional[str] = None) -> List[AgentMetadata]:
        """Searches for agents by author and location from the database."""
        logger.info(f"Searching for agents with author='{author}', location='{location}' in database.")
        
        conditions = []
        params = {}

        if author:
            conditions.append("author = :author")
            params["author"] = author
        if location:
            conditions.append("location = :location")
            params["location"] = location

        query = "SELECT * FROM agent_metadata"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        results = self._execute_query(query, params)
        return [AgentMetadata(**row) for row in results]
