from flask import request, jsonify
import json

from app import app
from services.service_project import *
from services.service_time_record import get_by_project
from dto.ProjectDto import ProjectDto


@app.route("/api/v1.0/projects", methods=["POST"])
def api_project_add():
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    response = add(ProjectDto.parseJson(data))
    return response


@app.route("/api/v1.0/projects", methods=["GET"])
def api_project_get_all():
    projects = get_all()
    return projects


@app.route("/api/v1.0/projects/<string:id>", methods=["GET"])
def api_project_get(id: int):
    response = get_one(id)
    return response


@app.route("/api/v1.0/projects/<string:id>", methods=["PUT"])
def api_project_update(id):
    # Logic to update a specific project by ID
    data = request.get_json()
    if not data:
        return get_response_json(id, False, "No JSON data", 400)

    response = update(ProjectDto.parseJson(data, id))
    return response


@app.route("/api/v1.0/projects/<string:id>", methods=["DELETE"])
def api_project_delete(id):
    response = delete(id)
    return response


@app.route("/api/v1.0/projects/<string:id>/records", methods=["GET"])
def api_project_get_records(id):
    records = get_by_project(id)
    return records
