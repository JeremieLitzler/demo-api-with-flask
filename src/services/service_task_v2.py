from flask import jsonify, request
from sqlalchemy.orm import scoped_session

from interfaces import IRepository, IService

from utils.api_utils import raise_business_error, handle_ex
from services.service_project_v2 import ProjectService
from dto.Task import TaskDto
from dao.models import Task
import dal.dal_task as dal_task


class TaskService:
    _repository: IRepository
    _projectService: IService

    def __init__(self, repository: IRepository, projectService: IService = None):
        self._repository = repository
        self._projectService = projectService

    def validate(self, data: TaskDto, checkProject=True):
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

        project = self._projectService.get_one(data.project_id, True)
        if project == None:
            raise_business_error(None, False, "Project doesn't exist", 422)

    def create(self, jsonData: dict) -> None:
        data = TaskDto.parseJson(jsonData)
        self.validate(data)

        try:
            # TODO: Feat > automap the Dto to Model
            new_task = Task()
            new_task.name = data.name
            new_task.project_id = data.project_id

            inserted_task = self._repository.add(new_task)
            return inserted_task, 201
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_task.create")

    def get_one(self, id: str, noJson=False) -> TaskDto:
        if id.strip() == "":
            raise_business_error(id, False, "ID is required", 422)

        try:
            task = self._repository.set_model(Task).fetch_one(id)
            if noJson:
                return task
            if task is None:
                raise_business_error(id, False, "Task not found", 404)

            return task
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_task.get_one")

    def get_all(self) -> list[TaskDto]:
        try:
            tasks = self._repository.set_model(Task).fetch_all()
            return tasks
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_task.get_all")

    # TODO > Feat: how do you notify the client that the project_id cannot be
    #              changed? http 400 if Dto contains the attribute?
    def update_one(self, id: str, jsonData: dict) -> None:
        try:
            task = self._repository.set_model(Task).fetch_one(id)
            if task == None:
                raise_business_error(id, False, "Task not found", 404)

            # TODO > Feat : check name not already taken

            data = TaskDto.parseJson(jsonData, id)

            if data.name is not None and data.name.strip() != "":
                task.name = data.name
            if data.completed is not None:
                task.completed = data.completed

            return self._repository.update(task)
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_task.update")

    # TODO > Feat: cannot delete a task if records exist for the task
    def delete_one(self, id: str):
        if id.strip() == "":
            raise_business_error(id, False, "ID is required", 422)

        try:
            result = self._repository.set_model(Task).delete(id)
            return "", 204
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_task.delete")
