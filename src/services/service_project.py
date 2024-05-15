from pathlib import Path
from flask import jsonify, request

import sqlite3
import os
import uuid
import json

from sqlalchemy.orm import scoped_session

from app import app
from utils.api_utils import get_response_json, raise_business_error, handle_ex
from dto.Project import ProjectDto
from dao.models import Project
import dal.dal_project as dal_project


def validate(data: ProjectDto):
    if data.name == None:
        raise_business_error(id, False, "Project name is required", 422)
    if data.name.strip() == "":
        raise_business_error(id, False, "Project name is empty", 422)
    if data.color == None:
        raise_business_error(id, False, "Color is required", 422)
    if data.color.strip() == "":
        raise_business_error(id, False, "Color is empty", 422)


def add(jsonData: dict) -> None:
    try:
        project_data = ProjectDto.parseJson(jsonData)
        # TODO: Feat > automap the Dto to Model
        validate(project_data)
        new_project = Project(name=project_data.name, color=project_data.color)
        inserted_project = dal_project.add(new_project)
        return inserted_project, 201
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling create_project")


def get_one(id: str, noJson=False) -> ProjectDto:
    if id.strip() == "":
        return get_response_json(id, False, "ID is required", 422)

    try:
        project = dal_project.fetch_one(id)
        if noJson:
            return project
        if project is None:
            return raise_business_error(id, False, "Project not found", 404)

        return project
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling get_project")


def get_all() -> list[ProjectDto]:
    try:
        projects = dal_project.fetch_all()
        return projects
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling get_projects")


def update_one(id: str, jsonData: dict) -> None:
    try:
        project = dal_project.fetch_one(id)
        if project == None:
            return raise_business_error(id, False, "Project not found", 404)

        project_data = ProjectDto.parseJson(jsonData, id)
        if project_data.name is not None:
            project.name = project_data.name
        if project_data.color is not None:
            project.color = project_data.color

        dal_project.save()
        return project
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling update_project")


def delete_one(id: str):
    if id.strip() == "":
        return get_response_json(id, False, "ID is required", 422)

    try:
        result = dal_project.delete(id)
        return "", 204
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling delete_project")
