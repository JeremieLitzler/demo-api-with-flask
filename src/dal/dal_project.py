from sqlalchemy.orm import sessionmaker

from app import app
from constants.environment_vars import *
from dal.models import Project

# from app import app

# engine = app.config[EnvironmentVariable.DATABASE_ENGINE]
session_db = app.config[EnvironmentVariable.SESSION_LOCAL]


def fetchAll():
    result = session_db.query(Project).all()
    return result
