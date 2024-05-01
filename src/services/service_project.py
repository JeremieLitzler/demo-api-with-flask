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


def add(project_data: ProjectDto) -> None:

    try:
        # TODO: Feat > automap the Dto to Model
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


def getOne(id: str, noJson=False) -> ProjectDto:
    try:
        project = dal_project.fetchOne(id)
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


def getAll() -> list[ProjectDto]:
    try:
        projects = dal_project.fetchAll()
        return jsonify(projects)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling get_projects")


def update(project_data: ProjectDto) -> None:
    try:
        project = dal_project.fetchOne(project_data.id)
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
        return get_response_json(id, True, message)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling delete_project")
