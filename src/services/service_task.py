from flask import jsonify, request
from pathlib import Path
import sqlite3
import os
import uuid
import json
from sqlalchemy.orm import scoped_session

from app import app
from utils.api_utils import get_response_json, raise_business_error, handle_ex
import services.service_project as service_project
from dto.Task import TaskDto
from dao.models import Task
import dal.dal_task as dal_task


def validate(data: TaskDto, checkProject=True):
    if data.name == None:
        raise_business_error(None, False, "Task name is required", 422)
    if data.name.strip() == "":
        raise_business_error(None, False, "Task name is empty", 422)

    if checkProject == False:
        return None

    if data.project_id == None:
        raise_business_error(None, False, "Project is required", 422)
    if data.project_id.strip() == "":
        raise_business_error(None, False, "Project is empty", 422)

    project = service_project.get_one(data.project_id, True)
    if project == None:
        raise_business_error(None, False, "Project doesn't exist", 422)

    return None


def create(jsonData: dict) -> None:
    data = TaskDto.parseJson(jsonData)
    result = validate(data)
    if result != None:
        return result

    try:
        # TODO: Feat > automap the Dto to Model
        new_task = Task()
        new_task.name = data.name
        new_task.project_id = data.project_id

        inserted_task = dal_task.add(new_task)
        return inserted_task, 201
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_task.create")


def get_one(id: str, noJson=False) -> TaskDto:
    if id.strip() == "":
        return get_response_json(id, False, "ID is required", 422)

    try:
        task = dal_task.fetch_one(id)
        if noJson:
            return project
        if task is None:
            return raise_business_error(id, False, "Task not found", 404)

        return task
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_task.get_one")


def get_all() -> list[TaskDto]:
    try:
        tasks = dal_task.fetch_all()
        return tasks
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_task.get_all")


# TODO > Feat: how do you notify the client that the project_id cannot be
#              changed? http 400 if Dto contains the attribute?
def update_one(id: str, jsonData: dict) -> None:
    try:
        task = dal_task.fetch_one(id)
        if task == None:
            return raise_business_error(id, False, "Task not found", 404)

        # TODO > Feat : check name not already taken

        data = TaskDto.parseJson(jsonData, id)

        if data.name is not None and data.name.strip() != "":
            task.name = data.name
        if data.completed is not None:
            task.completed = data.completed

        dal_task.save()

        return task
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_task.update")


# TODO > Feat: cannot delete a task if records exist for the task
def delete_one(id: str):
    if id.strip() == "":
        return get_response_json(id, False, "ID is required", 422)

    try:
        result = dal_task.delete(id)
        return "", 204
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_task.delete")
