# TODO > Feat: DRY the code a bit since all dal files are the same
#              Idea: how do you use generics in Python?
from sqlalchemy.orm import scoped_session

from app import app
from constants.environment_vars import EnvironmentVariable
from dao.models import Task

# from app import app

# engine = app.config[EnvironmentVariable.DATABASE_ENGINE]
session_db: scoped_session = app.config[EnvironmentVariable.SESSION_LOCAL]


# Commit changes, whether it is an INSERT or a UPDATE
def save():
    session_db.commit()


# Add a task
def add(task: Task):
    session_db.add(task)
    save()
    print(f"Inserted {task.name} to the DB")
    session_db.refresh(task)
    return task


# Get all the tasks
def fetch_all():
    result = session_db.query(Task).all()
    return result


# Get a task by id
def fetch_one(id: str):
    result = session_db.query(Task).filter_by(id=id)
    if result.count() == 1:
        return result.first()
    else:
        return None


def delete(id: str):
    task = fetch_one(id)
    if task is None:
        return False

    session_db.delete(task)
    session_db.commit()
    return True
