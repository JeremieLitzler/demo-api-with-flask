from pathlib import Path
from flask import jsonify, request

import sqlite3
import os
import uuid
import json

from sqlalchemy.orm import scoped_session

from interfaces import IRepository

from utils.api_utils import raise_business_error, handle_ex
from dto.Project import ProjectDto
from dao.models import Project


class ProjectService:
    _repository: IRepository

    def __init__(self, repository: IRepository):
        self._repository = repository

    def validate(self, data: ProjectDto):
        if data.name == None:
            raise_business_error(id, False, "Project name is required", 422)
        if data.name.strip() == "":
            raise_business_error(id, False, "Project name is empty", 422)
        if data.color == None:
            raise_business_error(id, False, "Color is required", 422)
        if data.color.strip() == "":
            raise_business_error(id, False, "Color is empty", 422)

    def add(self, jsonData: dict) -> None:
        try:
            project_data = ProjectDto.parseJson(jsonData)
            # TODO: Feat > automap the Dto to Model
            self.validate(project_data)
            new_project = Project(name=project_data.name, color=project_data.color)
            inserted_project = self._repository.add(new_project)
            return inserted_project, 201
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling create_project")

    def get_one(self, id: str, noJson=False) -> ProjectDto:
        if id.strip() == "":
            raise_business_error(id, False, "ID is required", 422)

        try:
            project = self._repository.set_model(Project).fetch_one(id)
            if noJson:
                return project
            if project is None:
                raise_business_error(id, False, "Project not found", 404)

            return project
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling get_project")

    def get_all(self) -> list[ProjectDto]:
        try:
            projects = self._repository.set_model(Project).fetch_all()
            return projects
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling get_projects")

    def update_one(self, id: str, jsonData: dict) -> None:
        try:
            project = self._repository.set_model(Project).fetch_one(id)
            if project == None:
                raise_business_error(id, False, "Project not found", 404)

            project_data = ProjectDto.parseJson(jsonData, id)
            if project_data.name is not None:
                project.name = project_data.name
            if project_data.color is not None:
                project.color = project_data.color

            self._repository.update()
            return project
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling update_project")

    def delete_one(self, id: str):
        if id.strip() == "":
            raise_business_error(id, False, "ID is required", 422)

        try:
            result = self._repository.set_model(Project).delete(id)
            return "", 204
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling delete_project")
