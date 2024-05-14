from flask import request, jsonify
import json

from app import app
from services.service_time_record import *
from dto.TimeRecordStartDto import TimeRecordStartDto
from dto.TimeRecordEndDto import TimeRecordEndDto


@app.route("/api/v1.0/records", methods=["POST"])
def api_record_add():
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    dto = TimeRecordStartDto.parseJson(data)
    response = start(dto)
    return response


@app.route("/api/v1.0/records/<string:id>", methods=["GET"])
def api_record_get(id: str):
    response = get_one(id)
    return response


@app.route("/api/v1.0/records/<string:id>/stop", methods=["PUT"])
def api_record_update_stop(id):
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    response = stop(id, TimeRecordEndDto.parseJson(data, id))
    return response


@app.route("/api/v1.0/records/<string:id>/notes", methods=["PUT"])
def api_record_update_notes(id):
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    response = update_notes(id, data.get("notes"))
    return response


@app.route("/api/v1.0/records/<string:id>", methods=["PUT"])
def api_record_update(id):
    data = request.get_json()
    if not data:
        return get_response_json(None, False, "No JSON data", 400)

    startDto = TimeRecordStartDto.parseJson(data, id)
    endDto = TimeRecordEndDto.parseJson(data, id)
    notes = data.get("notes")
    response = update(id, startDto, endDto, notes)
    return response


@app.route("/api/v1.0/records/<string:id>", methods=["DELETE"])
def api_record_delete(id):
    response = delete(id)
    return response
