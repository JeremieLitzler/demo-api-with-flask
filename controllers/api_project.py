from flask import request, jsonify
import json

from app import app
from services.service_project import *
from dto.ProjectDto import ProjectDto

@app.route('/api/v1.0/project', methods=['POST'])
def api_project_add():
    data = request.get_json()
    return create_project(ProjectDto.parseJson(data))

@app.route('/api/v1.0/project/all', methods=['GET'])
def api_project_get_all():
  projects = get_projects()
  project_dicts = [project._asdict() for project in projects]  # Convert to dictionaries
  return jsonify(project_dicts)

    
@app.route('/api/v1.0/project/<string:id>', methods=['GET'])
def api_project_get(id: int):
  project = get_project(id)
  if project:
    return jsonify(project._asdict())
  else:
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/v1.0/project/<string:id>', methods=['DELETE'])
def api_project_delete(id):
    # Logic to fetch specific project by ID
    return jsonify({'id': f'{id}', 'success': 'true', 'error': 'null'})

@app.route('/api/v1.0/project/<string:id>', methods=['PUT'])
def api_project_update(id):
    # Logic to update a specific project by ID
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data'}), 400

    updated_project = update_project(ProjectDto.parseJson(data, id))
    return jsonify(updated_project._asdict())
