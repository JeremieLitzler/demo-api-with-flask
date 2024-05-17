import os
from sqlalchemy import create_engine
from dao.models import Model
from constants.environment_vars import EnvironmentVariable


def init_engine(base_dir: str, useRemote: bool = False):
    """Load the engine

    Args:
        base_dir (str): The base directory where the database is stored

    Returns:
        object: The engine
    """
    connection_string = f"sqlite:///{base_dir}{os.sep}..{os.sep}db{os.sep}sqlalchemy.db"
    if useRemote:
        # See https://support.cloudways.com/en/articles/5124841-how-to-setup-mysql-remote-connection-to-database
        # See also https://stackoverflow.com/a/29429717
        # You need to install pymysql
        db_host = os.getenv(EnvironmentVariable.PY_DB_HOST)
        db_name = os.getenv(EnvironmentVariable.PY_DB_NAME)
        db_user_name = os.getenv(EnvironmentVariable.PY_DB_USER)
        db_user_pass = os.getenv(EnvironmentVariable.PY_DB_PASSWORD)

        connection_string = (
            f"mysql+pymysql://{db_user_name}:{db_user_pass}@{db_host}/{db_name}"
        )
        print("connecting to remote MySql DB")
    else:
        print("connecting to remote SQLLite DB")

    engine = create_engine(connection_string, echo=True)
    return engine


def reset_database(base_dir: str, useRemote: bool = False):
    """Reset the database by dropping all tables

    Args:
        base_dir (str): The base directory where the database is stored
    """
    Model.metadata.drop_all(init_engine(base_dir, useRemote))


def init_database(base_dir: str, useRemote: bool = False):
    """Initialize the database by creating the tables that needs to be created.
    It doesn't try to recreate what already exists.

    See https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all

    Args:
        base_dir (str): _description_
    """
    Model.metadata.create_all(init_engine(base_dir, useRemote))
