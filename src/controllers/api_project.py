from flask import request, jsonify
from flask_restx import Resource, fields
import json

from api_swagger import api
from services.service_project import *
from services.service_time_record import get_by_project
from dto.Project import (
    ProjectDto,
    ProjectRequestSwaggerModel,
    ProjectResponseSwaggerModel,
)
from dto.TimeRecord import RecordResponseSwaggerModel

ns = api.namespace("api/v1.0/projects", description="Project operations")


@ns.route("/")
class ProjectList(Resource):
    @ns.doc("api_project_add")
    @ns.expect(ProjectRequestSwaggerModel)
    @ns.marshal_with(ProjectResponseSwaggerModel, code=201)
    @ns.response(422, "Payload is invalid. See details in response.")
    def post(self):
        """Create a new project"""
        response = add(api.payload)
        return response

    @ns.doc("api_project_get_all")
    @ns.marshal_with(ProjectResponseSwaggerModel)
    def get(self):
        """List all the projects"""
        projects = get_all()
        return projects


@ns.route("/<string:id>")
@ns.response(404, "Project not found")
@ns.param("id", "The project identifier")
class Project(Resource):

    @ns.doc("api_project_get_one")
    @ns.marshal_with(ProjectResponseSwaggerModel)
    def get(self, id):
        """Retrieve a single project"""
        response = get_one(id)
        return response

    @ns.doc("api_project_update")
    @ns.expect(ProjectRequestSwaggerModel)
    @ns.marshal_with(ProjectResponseSwaggerModel)
    @ns.response(422, "Payload is invalid. See details in response.")
    def put(self, id):
        """Update a project"""
        response = update_one(id, api.payload)
        return response

    """Delete a project"""

    @ns.doc("api_project_delete")
    @ns.response(204, "Project deleted")
    def delete(self, id):
        response = delete_one(id)
        return response


@ns.route("/<string:id>/records")
@ns.response(404, "Project not found")
@ns.param("id", "The project identifier")
class ProjectRecords(Resource):
    @ns.doc("api_project_get_records")
    @ns.marshal_with(RecordResponseSwaggerModel)
    def get(self, id):
        """List all records of the project"""
        records = get_by_project(id)
        return records
