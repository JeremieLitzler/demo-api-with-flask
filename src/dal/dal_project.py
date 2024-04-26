from sqlalchemy.orm import scoped_session

from app import app
from constants.environment_vars import *
from dal.models import Project

# from app import app

# engine = app.config[EnvironmentVariable.DATABASE_ENGINE]
session_db: scoped_session = app.config[EnvironmentVariable.SESSION_LOCAL]


# Commit changes, whether it is an INSERT or a UPDATE
def save():
    session_db.commit()


# Add a project
def add(project: Project):
    session_db.add(project)
    save()
    print(f"Inserted {project.name} to the DB")


# Get all the projects
def fetchAll():
    result = session_db.query(Project).all()
    return result


# Get a project by id
def fetchOne(id: str):
    result = session_db.query(Project).filter_by(id=id)
    if result.count() == 1:
        return result.first()
    else:
        return None


def delete(id: str):
    project = fetchOne(id)
    if project is None:
        return False

    session_db.delete(project)
    session_db.commit()
    return True
