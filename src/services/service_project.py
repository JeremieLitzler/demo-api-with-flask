from flask import jsonify, request

from pathlib import Path

import sqlite3
import os
import uuid
import json

from sqlalchemy.orm import scoped_session

from app import app

from utils.api_utils import get_response_json

from dto.ProjectDto import ProjectDto

from dao.models import Project

import dal.dal_project as dal_project


def validate_project_name(name: str, id: str = None):
    if name == None:
        return get_response_json(id, False, "Project name is required", 422)
    if name.strip() == "":
        return get_response_json(id, False, "Project name is empty", 422)

    return None


def validate_project_color(color: str, id: str = None):
    if color == None:
        return get_response_json(id, False, "Color is required", 422)
    if color.strip() == "":
        return get_response_json(id, False, "Color is empty", 422)

    return None


def validate(project_data: ProjectDto):
    result = validate_project_name(project_data.name, project_data.id)
    if result is not None:
        return result

    result = validate_project_color(project_data.color, project_data.id)
    return result


def add(project_data: ProjectDto) -> None:
    try:

        # TODO: Feat > automap the Dto to Model
        validation = validate(project_data)
        if validation is not None:
            return validation

        new_project = Project(name=project_data.name, color=project_data.color)
        dal_project.add(new_project)

        # Return True if at least one row was added

        message = "null" if True else "No record affected"

        return get_response_json(new_project.id, True, message)

    except Exception as ex:

        print(ex)

        return get_response_json(id, False, ex)

    finally:

        print("finished calling create_project")


def get_one(id: str, noJson=False) -> ProjectDto:

    try:

        project = dal_project.fetch_one(id)

        if noJson:
            return project

        if project == None:

            return get_response_json(id, False, "Project not found", 404)
        else:

            return jsonify(project)

    except Exception as ex:

        print(ex)

        return get_response_json(id, False, ex, 500)

    finally:

        print("finished calling get_project")


def get_all() -> list[ProjectDto]:

    try:

        projects = dal_project.fetch_all()

        return jsonify(projects)

    except Exception as ex:

        print(ex)

        return get_response_json(id, False, ex)

    finally:

        print("finished calling get_projects")


def update(project_data: ProjectDto) -> None:

    try:

        project = dal_project.fetch_one(project_data.id)

        if project == None:

            return get_response_json(id, False, "Project not found", 404)

        if project_data.name is not None:

            project.name = project_data.name

        if project_data.color is not None:

            project.color = project_data.color

        dal_project.save()

        return jsonify(project)

    except Exception as ex:

        print(ex)

        return get_response_json(id, False, ex)

    finally:

        print("finished calling update_project")


def delete(id: str) -> bool:

    try:

        result = dal_project.delete(id)

        message = "Project deleted successfully" if result else "No record affected"

        return get_response_json(id, True, message, 204)

    except Exception as ex:

        print(ex)

        return get_response_json(id, False, ex)

    finally:

        print("finished calling delete_project")
