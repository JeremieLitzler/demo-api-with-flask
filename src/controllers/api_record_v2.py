import json
from flask import request, jsonify
from flask_restx import Resource, fields
from sqlalchemy.orm import scoped_session

from api_swagger import api
from app import app
from constants.environment_vars import EnvironmentVariable
from services.service_record_v2 import RecordService
from services.service_project_v2 import ProjectService
from services.service_task_v2 import TaskService
from dal.sqla_repository import SQLAlchemyRepository
from dto.TimeRecord import (
    TimeRecordStartDto,
    TimeRecordEndDto,
    RecordStartRequestSwaggerModel,
    RecordStopRequestSwaggerModel,
    RecordNotesRequestSwaggerModel,
    RecordUpdateRequestSwaggerModel,
    RecordResponseSwaggerModel,
)

session_db: scoped_session = app.config[EnvironmentVariable.SESSION_LOCAL]
repository: SQLAlchemyRepository = SQLAlchemyRepository(session_db)


ns = api.namespace("api/v2.0/records", description="Time record operations")
_recordService = RecordService(
    repository, ProjectService(repository), TaskService(repository)
)


@ns.route("/")
class RecordList(Resource):
    @ns.doc("api_record_add")
    @ns.expect(RecordStartRequestSwaggerModel)
    @ns.marshal_with(RecordResponseSwaggerModel, code=201)
    @ns.response(422, "Record payload is invalid. See details in response.")
    def post(self):
        """Create a new record"""
        response = _recordService.start(api.payload)
        return response

    @ns.doc("api_record_get_all")
    @ns.marshal_with(RecordResponseSwaggerModel)
    def get(self):
        """List all the records"""
        projects = _recordService.get_all()
        return projects


@ns.route("/<string:id>")
@ns.response(404, "Record not found")
@ns.param("id", "The record identifier")
class Record(Resource):
    @ns.doc("api_record_get_one")
    @ns.marshal_with(RecordResponseSwaggerModel)
    def get(self, id):
        """Retrieve a single record"""
        response = _recordService.get_one(id)
        return response

    @ns.doc("api_record_update")
    @ns.expect(RecordUpdateRequestSwaggerModel)
    @ns.marshal_with(RecordResponseSwaggerModel)
    @ns.response(422, "Record payload is invalid. See details in response.")
    def put(self, id):
        """Update a record"""
        response = _recordService.update_one(id, api.payload)
        return response

    @ns.doc("api_record_delete")
    @ns.response(204, "Record deleted")
    def delete(self, id):
        """Delete a record"""
        response = _recordService.delete_one(id)
        return response


@ns.route("/<string:id>/stop")
@ns.response(404, "Record not found")
@ns.param("id", "The record identifier")
class RecordStop(Resource):

    @ns.doc("api_record_stop")
    @ns.expect(RecordStopRequestSwaggerModel)
    @ns.marshal_with(RecordResponseSwaggerModel)
    @ns.response(422, "Record payload is invalid. See details in response.")
    def put(self, id):
        """Stop a record"""
        response = _recordService.stop(id, api.payload)
        return response


@ns.route("/<string:id>/notes")
@ns.response(404, "Record not found")
@ns.param("id", "The record identifier")
class RecordNotes(Resource):

    @ns.doc("api_record_notes")
    @ns.expect(RecordNotesRequestSwaggerModel)
    @ns.marshal_with(RecordResponseSwaggerModel)
    @ns.response(422, "Record payload is invalid. See details in response.")
    def put(self, id):
        """Update a record´s notes"""
        response = _recordService.update_notes(id, api.payload)
        return response
