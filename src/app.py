import os

from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

from constants.environment_vars import EnvironmentVariable

# from dal.main import init_engine
from dal.main import init_database, reset_database, init_engine

load_dotenv()

env = os.getenv(EnvironmentVariable.ENVIRONMENT)

# Create the Flask application instance
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if env == "dev":
    print("Environment is dev")
    # Create the database engine (dependency injection)
    app.config[EnvironmentVariable.DATABASE_ENGINE] = init_engine(BASE_DIR)

    # Create a session maker using the injected engine
    SessionLocal = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=app.config[EnvironmentVariable.DATABASE_ENGINE],
        )
    )

    app.config[EnvironmentVariable.SESSION_LOCAL] = SessionLocal

    # TODO: drop the database
    reset_database(BASE_DIR)
    # TODO: and recreate it
    init_database(BASE_DIR)

    if env == "production":
        print("Environment is production")
