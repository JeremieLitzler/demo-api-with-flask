import os
from sqlalchemy import create_engine
from dao.models import Model


def init_engine(base_dir: str):
    """Load the engine

    Args:
        base_dir (str): The base directory where the database is stored

    Returns:
        object: The engine
    """
    db_file_name = f"sqlite:///{base_dir}{os.sep}..{os.sep}db{os.sep}sqlalchemy.db"
    engine = create_engine(db_file_name, echo=True)
    return engine


def reset_database(base_dir: str):
    """Reset the database by dropping all tables

    Args:
        base_dir (str): The base directory where the database is stored
    """
    Model.metadata.drop_all(init_engine(base_dir))


def init_database(base_dir: str):
    """Initialize the database by creating the tables that needs to be created.
    It doesn't try to recreate what already exists.

    See https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all

    Args:
        base_dir (str): _description_
    """
    Model.metadata.create_all(init_engine(base_dir))
