from sqlalchemy.orm import scoped_session

from app import app
from constants.environment_vars import *
from dal.models import Project

# from app import app

# engine = app.config[EnvironmentVariable.DATABASE_ENGINE]
session_db: scoped_session = app.config[EnvironmentVariable.SESSION_LOCAL]


def add(project: Project):
    session_db.add(project)
    save()
    print(f"Inserted {project.name} to the DB")


def fetchAll():
    result = session_db.query(Project).all()
    return result


def fetchOne(id: str):
    result = session_db.query(Project).filter_by(id=id)
    if result.count() == 1:
        return result.first()
    else:
        return None


def save():
    session_db.commit()
