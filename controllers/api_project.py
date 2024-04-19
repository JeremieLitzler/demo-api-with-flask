from flask import request, jsonify
from app import app
# GET /project
@app.route('/api/v1.0/project/all', methods=['GET'])
def api_project_get_all():
    # Fetch data from a database or other source
    return jsonify([])  # Convert data to JSON format

# POST /project
@app.route('/api/v1.0/project', methods=['POST'])
def api_project_add():
    # Logic to add a project
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Process the data (e.g., access values):
    name = data.get('name')

    # TODO: And add the new record to a db
    
    # Return the data
    return jsonify({'message': f'Added project: {name}'})

    
# GET /project/:id
@app.route('/api/v1.0/project/<int:id>', methods=['GET'])
def api_project_get(id: int):
    # Logic to fetch specific project by ID
    return jsonify({})

# DELETE /project/:id
@app.route('/api/v1.0/project/<int:id>', methods=['DELETE'])
def api_project_delete(id):
    # Logic to fetch specific project by ID
    return jsonify({'id': f'{id}', 'success': 'true', 'error': 'null'})

# PUT /project/:id
@app.route('/api/v1.0/project/<int:id>', methods=['PUT'])
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
