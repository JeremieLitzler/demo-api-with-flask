from flask import request, jsonify
from flask_restx import Resource, fields
import json

from api_swagger import api
from services.service_time_record import *
from dto.TimeRecord import (
    TimeRecordStartDto,
    TimeRecordEndDto,
    TimeRecordRequestSwaggerModel,
    TimeRecordResponseSwaggerModel,
)

ns = api.namespace("api/v1.0/records", description="Time record operations")


@ns.route("/")
class RecordList(Resource):
    @ns.doc("api_record_add")
    @ns.expect(TimeRecordRequestSwaggerModel)
    @ns.marshal_with(TimeRecordResponseSwaggerModel, code=201)
    def post(self):
        """Create a new record"""
        response = start(api.payload)
        return response

    @ns.doc("api_record_get_all")
    @ns.marshal_with(TimeRecordResponseSwaggerModel)
    def get(self):
        """List all the records"""
        projects = get_all()
        return projects


@ns.route("/<string:id>")
@ns.response(404, "Record not found")
@ns.param("id", "The record identifier")
class Record(Resource):
    """Retrieve a single record"""

    @ns.doc("api_record_get_one")
    @ns.marshal_with(TimeRecordResponseSwaggerModel)
    def get(self, id):
        response = get_one(id)
        return response

    """Update a record"""

    @ns.doc("api_record_update")
    @ns.marshal_with(TimeRecordResponseSwaggerModel)
    def put(self, id):
        response = update_one(id, api.payload)
        return response

    """Delete a record"""

    @ns.doc("api_record_delete")
    @ns.response(204, "Record deleted")
    def delete(self, id):
        response = delete_one(id)
        return response


@ns.route("/<string:id>/stop")
@ns.response(404, "Record not found")
@ns.param("id", "The record identifier")
class RecordStop(Resource):
    """Stop a record"""

    @ns.doc("api_record_stop")
    @ns.marshal_with(TimeRecordResponseSwaggerModel)
    def put(self, id):
        response = stop(id, api.payload)
        return response


@ns.route("/<string:id>/notes")
@ns.response(404, "Record not found")
@ns.param("id", "The record identifier")
class RecordNotes(Resource):
    """Update a record´s notes"""

    @ns.doc("api_record_notes")
    @ns.marshal_with(TimeRecordResponseSwaggerModel)
    def put(self, id):
        response = update_notes(id, api.payload)
        return response
