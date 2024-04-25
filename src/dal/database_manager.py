import os

from sqlalchemy import create_engine
from dotenv import load_dotenv
from constants.environment_vars import EnvironmentVariable

load_dotenv()

DATABASE_URL = os.getenv(EnvironmentVariable.DATABASE_URL)


class DatabaseManager:
    """Singleton class to manage database connection"""

    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Create engine on first instance creation (i.e., at launch)
            cls._engine = create_engine(DATABASE_URL)
        return cls._instance

    @property
    def engine(self):
        return self._engine
