from flask import request, jsonify
import json

from app import app
from services.service_time_record import *
from dto.TimeRecordStartDto import TimeRecordStartDto
from dto.TimeRecordEndDto import TimeRecordEndDto


@app.route("/api/v1.0/record", methods=["POST"])
def api_record_add():
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    dto = TimeRecordStartDto.parseJson(data)
    response = start(dto)
    return response


@app.route("/api/v1.0/record/byTask/<string:id>", methods=["GET"])
def api_record_get_by_task(id):
    records = get_by_task(id)
    return records


@app.route("/api/v1.0/record/byProject/<string:id>", methods=["GET"])
def api_record_get_by_project(id):
    records = get_by_project(id)
    return records


@app.route("/api/v1.0/record/<string:id>", methods=["GET"])
def api_record_get(id: str):
    response = get_one(id)
    return response


@app.route("/api/v1.0/record/<string:id>/stop", methods=["PUT"])
def api_record_update_stop(id):
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    response = stop(id, TimeRecordEndDto.parseJson(data, id))
    return response


@app.route("/api/v1.0/record/<string:id>/notes", methods=["PUT"])
def api_record_update_notes(id):
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    response = update_notes(id, data.get("notes"))
    return response


@app.route("/api/v1.0/record/<string:id>", methods=["DELETE"])
def api_record_delete(id):
    response = delete(id)
    return response
