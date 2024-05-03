# TODO > Feat: DRY the code a bit since all dal files are the same
#              Idea: how do you use generics in Python?
from sqlalchemy.orm import scoped_session

from app import app
from constants.environment_vars import EnvironmentVariable
from dao.models import TimeRecord

# from app import app

# engine = app.config[EnvironmentVariable.DATABASE_ENGINE]
session_db: scoped_session = app.config[EnvironmentVariable.SESSION_LOCAL]


# Commit changes, whether it is an INSERT or a UPDATE
def save():
    session_db.commit()


# Add a record
def add(record: TimeRecord):
    session_db.add(record)
    save()
    print(f"Inserted {record.id} to the DB")


# Get record or records by colum
def fetch_by(colum: str, id: str):
    result = None
    if colum == "task_id":
        result = session_db.query(TimeRecord).filter_by(task_id=id)
        return result.all()
    if colum == "project_id":
        result = session_db.query(TimeRecord).filter_by(project_id=id)
        return result.all()

    if colum == "id":
        result = session_db.query(TimeRecord).filter_by(id=id)

    if result.count() == 1:
        return result.first()
    else:
        return None


def delete(id: str):
    task = fetch_by("id", id)
    if task is None:
        return False

    session_db.delete(task)
    session_db.commit()
    return True
