from flask import request, jsonify
import json

from app import app
from services.service_task import *
from dto.TaskDto import TaskDto


@app.route("/api/v1.0/tasks", methods=["POST"])
def api_task_add():
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    response = create(TaskDto.parseJson(data))
    return response


@app.route("/api/v1.0/tasks", methods=["GET"])
def api_task_get_all():
    tasks = get_all()
    return tasks


@app.route("/api/v1.0/tasks/<string:id>", methods=["GET"])
def api_task_get(id: int):
    response = get_one(id)
    return response


@app.route("/api/v1.0/tasks/<string:id>", methods=["PUT"])
def api_task_update(id):
    # Logic to update a specific task by ID
    data = request.get_json()
    if not data:
        return get_response_json(id, False, "No JSON data", 400)

    response = update(TaskDto.parseJson(data, id))
    return response


@app.route("/api/v1.0/tasks/<string:id>", methods=["DELETE"])
def api_task_delete(id):
    response = delete(id)
    return response
