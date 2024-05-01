from flask import jsonify, request
from pathlib import Path
import sqlite3
import os
import uuid
import json
from sqlalchemy.orm import scoped_session

from app import app
from utils.api_utils import get_response_json
from dto.TaskDto import TaskDto
from dao.models import Task
import dal.dal_task as dal_task
import services.service_project as service_project


def validate(data: TaskDto, checkProject=True):
    if data.name == None:
        return get_response_json(None, False, "Task name is required", 400)
    if data.name.strip() == "":
        return get_response_json(None, False, "Task name is empty", 400)

    if checkProject == False:
        return

    if data.project_id == None:
        return get_response_json(None, False, "Project is required", 400)
    if data.project_id.strip() == "":
        return get_response_json(None, False, "Project is empty", 400)

    project = service_project.getOne(data.project_id, True)
    if project == None:
        return get_response_json(None, False, "Project doesn't exist", 400)


def create(data: TaskDto) -> None:

    validate(data)

    try:
        # TODO: Feat > automap the Dto to Model
        newTask = Task()
        newTask.name = data.name
        newTask.project_id = data.project_id

        dal_task.add(newTask)

        # Return True if at least one row was added
        message = "null" if True else "No record affected"
        return get_response_json(newTask.id, True, message)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling service_task.create")


def getOne(id: str, noJson=False) -> TaskDto:
    if id.strip() == "":
        return get_response_json(id, False, "ID is required", 400)

    try:
        task = dal_task.fetchOne(id)
        if task == None:
            return get_response_json(id, False, "Task not found", 404)
        else:
            return jsonify(task)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex, 500)
    finally:
        print("finished calling service_task.getOne")


def getAll() -> list[TaskDto]:
    try:
        tasks = dal_task.fetchAll()
        return jsonify(tasks)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling service_task.getAll")


# TODO > Feat: how do you notify the client that the project_id cannot be
#              changed? http 400 if Dto contains the attribute?
def update(data: TaskDto) -> None:
    validate(data, False)
    try:
        task = dal_task.fetchOne(data.id)
        if task == None:
            return get_response_json(id, False, "Task not found", 404)

        # TODO > Feat : check name not already taken

        if data.name is not None:
            task.name = data.name
        if data.completed is not None:
            task.completed = data.completed

        dal_task.save()

        return jsonify(task)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling service_task.update")


# TODO > Feat: cannot delete a task if records exist for the task
def delete(id: str) -> bool:
    if id.strip() == "":
        return get_response_json(id, False, "ID is required", 400)

    try:
        result = dal_task.delete(id)
        message = "Task deleted successfully" if result else "No record affected"
        return get_response_json(id, True, message)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling service_task.delete")
