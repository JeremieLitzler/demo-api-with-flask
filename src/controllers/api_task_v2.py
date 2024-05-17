import json
from flask import request, jsonify
from flask_restx import Resource, fields
from sqlalchemy.orm import scoped_session

from api_swagger import api
from app import app
from constants.environment_vars import EnvironmentVariable
from services.service_task_v2 import TaskService
from services.service_record_v2 import RecordService
from services.service_project_v2 import ProjectService

from dal.sqla_repository import SQLAlchemyRepository
from dto.Task import TaskDto, TaskRequestSwaggerModel, TaskResponseSwaggerModel
from dto.TimeRecord import RecordResponseSwaggerModel

session_db: scoped_session = app.config[EnvironmentVariable.SESSION_LOCAL]
repository: SQLAlchemyRepository = SQLAlchemyRepository(session_db)

ns = api.namespace("api/v2.0/tasks", description="Task operations")
_taskService = TaskService(repository, ProjectService(repository))


@ns.route("/")
class TaskList(Resource):
    @ns.doc("api_task_add")
    @ns.expect(TaskRequestSwaggerModel)
    @ns.marshal_with(TaskResponseSwaggerModel, code=201)
    @ns.response(422, "Payload is invalid. See details in response.")
    def post(self):
        """Create a new task"""
        response = _taskService.create(api.payload)
        return response

    @ns.doc("api_task_get_all")
    @ns.marshal_with(TaskResponseSwaggerModel)
    def get(self):
        """List all the tasks"""
        tasks = _taskService.get_all()
        return tasks


@ns.route("/<string:id>")
@ns.response(404, "Task not found")
@ns.param("id", "The task identifier")
class Task(Resource):

    @ns.doc("api_task_get_one")
    @ns.marshal_with(TaskResponseSwaggerModel)
    def get(self, id):
        """Retrieve a single task"""
        response = _taskService.get_one(id)
        return response

    @ns.doc("api_task_update")
    @ns.expect(TaskRequestSwaggerModel)
    @ns.marshal_with(TaskResponseSwaggerModel)
    @ns.response(422, "Payload is invalid. See details in response.")
    def put(self, id):
        """Update a task"""
        response = _taskService.update_one(id, api.payload)
        return response

    @ns.doc("api_task_delete")
    @ns.response(204, "Task deleted")
    def delete(self, id):
        """Delete a task"""
        response = _taskService.delete_one(id)
        return response


@ns.route("/<string:id>/records")
@ns.response(404, "Task not found")
@ns.param("id", "The task identifier")
class TaskRecords(Resource):
    @ns.doc("api_task_get_records")
    @ns.marshal_with(RecordResponseSwaggerModel)
    def get(self, id):
        """List all records of the task"""
        records = RecordService(repository).get_by_task(id)
        return records
