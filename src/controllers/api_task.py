from flask import request, jsonify
from flask_restx import Resource, fields
import json

from api_swagger import api
from services.service_task import *
from services.service_time_record import get_by_task
from dto.Task import TaskDto, TaskSwaggerModel
from dto.TimeRecord import TimeRecordResponseSwaggerModel

ns = api.namespace("api/v1.0/tasks", description="Task operations")


@ns.route("/")
class TaskList(Resource):
    @ns.doc("api_task_add")
    @ns.expect(TaskSwaggerModel)
    @ns.marshal_with(TaskSwaggerModel, code=201)
    def post(self):
        """Create a new task"""
        response = create(api.payload)
        return response

    @ns.doc("api_task_get_all")
    @ns.marshal_with(TaskSwaggerModel)
    def get(self):
        """List all the tasks"""
        tasks = get_all()
        return tasks


@ns.route("/<string:id>")
@ns.response(404, "Task not found")
@ns.param("id", "The task identifier")
class Task(Resource):
    """Retrieve a single task"""

    @ns.doc("api_task_get_one")
    @ns.marshal_with(TaskSwaggerModel)
    def get(self, id):
        response = get_one(id)
        return response

    """Update a task"""

    @ns.doc("api_task_update")
    @ns.marshal_with(TaskSwaggerModel)
    def put(self, id):
        # Logic to update a specific task by ID
        response = update_one(id, api.payload)
        return response

    """Delete a task"""

    @ns.doc("api_task_delete")
    @ns.response(204, "Task deleted")
    def delete(self, id):
        response = delete_one(id)
        return response


@ns.route("/<string:id>/records")
@ns.response(404, "Task not found")
@ns.param("id", "The task identifier")
class TaskRecords(Resource):
    @ns.doc("api_task_get_records")
    @ns.marshal_with(TimeRecordResponseSwaggerModel)
    def get(self, id):
        """List all records of the task"""
        records = get_by_task(id)
        return records
