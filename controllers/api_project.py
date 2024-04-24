from flask import request, jsonify
import json

from app import app
from services.service_project import *
from dto.ProjectDto import ProjectDto

@app.route('/api/v1.0/project', methods=['POST'])
def api_project_add():
  data = request.get_json()
  response = create_project(ProjectDto.parseJson(data))
  return response

@app.route('/api/v1.0/project/all', methods=['GET'])
def api_project_get_all():
  projects = get_projects()
  project_dicts = [project._asdict() for project in projects]  # Convert to dictionaries
  return jsonify(project_dicts)

    
@app.route('/api/v1.0/project/<string:id>', methods=['GET'])
def api_project_get(id: int):
  response = get_project(id)
  return response

@app.route('/api/v1.0/project/<string:id>', methods=['PUT'])
def api_project_update(id):
  # Logic to update a specific project by ID
  data = request.get_json()
  if not data:
      return jsonify({'error': 'No JSON data'}), 400

  response = update_project(ProjectDto.parseJson(data, id))
  return response

@app.route('/api/v1.0/project/<string:id>', methods=['DELETE'])
def api_project_delete(id):
  response = delete_project(id)
  return response
