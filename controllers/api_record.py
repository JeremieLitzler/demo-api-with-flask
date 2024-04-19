from flask import request, jsonify
from app import app
# GET /record
@app.route('/api/v1.0/record/all', methods=['GET'])
def api_record_get_all():
    # Fetch data from a database or other source
    return jsonify([])  # Convert data to JSON format

# POST /record
@app.route('/api/v1.0/record', methods=['POST'])
def api_record_add():
    # Logic to add a record
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Process the data (e.g., access values):
    name = data.get('name')

    # TODO: And add the new record to a db
    
    # Return the data
    return jsonify({'message': f'Added record: {name}'})

    
# GET /record/:id
@app.route('/api/v1.0/record/<int:id>', methods=['GET'])
def api_record_get(id: int):
    # Logic to fetch specific record by ID
    return jsonify({})

# DELETE /record/:id
@app.route('/api/v1.0/record/<int:id>', methods=['DELETE'])
def api_record_delete(id):
    # Logic to fetch specific record by ID
    return jsonify({'id': f'{id}', 'success': 'true', 'error': 'null'})

# PUT /record/:id
@app.route('/api/v1.0/record/<int:id>', methods=['PUT'])
def api_record_update(id):
    # Logic to update a specific record by ID
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Process the data (e.g., access values):
    name = data.get('name')

    # TODO: And add the new record to a db
    
    # Return the data
    return jsonify({'id': f'{id}', 'success': 'true', 'error': 'null'})
