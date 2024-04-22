from flask import request, jsonify
import json

from app import app
from services.service_project import *
from dto.ProjectData import ProjectData

@app.route('/api/v1.0/project', methods=['POST'])
def api_project_add():
    project_data = request.get_json()
    name = project_data.get('name')
    color = project_data.get('color')
    isArchived = project_data.get('isArchived', False)
    new_project = ProjectData(name, color, isArchived)
    return create_project(new_project)

@app.route('/api/v1.0/project/all', methods=['GET'])
def api_project_get_all():
    # Fetch data from a database or other source
    return jsonify()  # Convert data to JSON format

    
@app.route('/api/v1.0/project/<string:id>', methods=['GET'])
def api_project_get(id: int):
  project = get_project(id)
  if project:
    project_dict = {'id': project.id, 'name': project.name, 'color': project.color, 'isArchived': bool(project.isArchived)}
    return jsonify(project_dict)
  else:
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/v1.0/project/<string:id>', methods=['DELETE'])
def api_project_delete(id):
    # Logic to fetch specific project by ID
    return jsonify({'id': f'{id}', 'success': 'true', 'error': 'null'})

@app.route('/api/v1.0/project/<string:id>', methods=['PUT'])
def api_project_update(id):
    # Logic to update a specific project by ID
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Process the data (e.g., access values):
    name = data.get('name')

    # TODO: And add the new record to a db
    
    # Return the data
    return jsonify({'id': f'{id}', 'success': 'true', 'error': 'null'})
