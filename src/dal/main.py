from sqlalchemy import create_engine
from dal.database_manager import DatabaseManager
from dal.models import *
import os
from dal.models import Model


def init_engine(base_dir: str):
    db_file_name = f"sqlite:///{base_dir}{os.sep}..{os.sep}db{os.sep}sqlalchemy.db"
    engine = create_engine(db_file_name, echo=True)
    return engine


def reset_database(base_dir: str):
    Model.metadata.drop_all(init_engine(base_dir))


def init_database(base_dir: str):
    Model.metadata.create_all(init_engine(base_dir))
