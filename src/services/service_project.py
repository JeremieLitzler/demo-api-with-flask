from flask import jsonify, request
from pathlib import Path
import sqlite3
import os
import uuid
import json
from sqlalchemy.orm import scoped_session

from app import app
from dto.ProjectDto import ProjectDto
from utils.validators import validate_required_properties
from utils.reflection import get_tuple_from_type
from utils.db_utils import row2dict
from utils.json_utils import new_alchemy_encoder_recursive_selective
import dal.dal_project as dal_project
from dal.models import Project
from constants.environment_vars import EnvironmentVariable

_session_db: scoped_session = app.config[EnvironmentVariable.SESSION_LOCAL]


def get_response_json(id: int, success: bool, message: str = "null"):
    return jsonify({"id": f"{id}", "success": f"{success}", "message": f"{message}"})


def create_project(project_data: ProjectDto) -> None:

    try:
        # Replace 'project_data.db' with your desired database filename
        newProject = Project(name=project_data.name, color=project_data.color)
        dal_project.add(newProject)

        # Return True if at least one row was added
        message = "null" if True else "No record affected"
        return get_response_json(newProject.id, True, message)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling create_project")


def get_project(project_id: str) -> ProjectDto:
    try:
        project = dal_project.fetchOne(project_id)
        if project == None:
            return jsonify({"message": "Project not found"}), 404
        else:
            return jsonify(project)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling get_project")


def get_projects() -> list[ProjectDto]:
    try:
        projects = dal_project.fetchAll()
        return jsonify(projects)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling get_projects")


def update_project(project_data: ProjectDto) -> None:
    try:
        project = dal_project.fetchOne(project_data.id)
        if project == None:
            return jsonify({"message": "Project not found"}), 404

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


def delete_project(id: str) -> bool:
    try:
        result = dal_project.delete(id)
        message = "" if result else "No record affected"
        return get_response_json(id, True, message)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling delete_project")
