from flask import request, jsonify
from app import app


# GET /task
@app.route("/api/v1.0/task/all", methods=["GET"])
def api_task_get_all():
    # Fetch data from a database or other source
    return jsonify([])  # Convert data to JSON format


# POST /task
@app.route("/api/v1.0/task", methods=["POST"])
def api_task_add():
    # Logic to add a task
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Process the data (e.g., access values):
    name = data.get("name")

    # TODO: And add the new record to a db

    # Return the data
    return jsonify({"message": f"Added task: {name}"})


# GET /task/:id
@app.route("/api/v1.0/task/<int:id>", methods=["GET"])
def api_task_get(id: int):
    # Logic to fetch specific task by ID
    return jsonify({})


# DELETE /task/:id
@app.route("/api/v1.0/task/<int:id>", methods=["DELETE"])
def api_task_delete(id):
    # Logic to fetch specific task by ID
    return jsonify({"id": f"{id}", "success": "true", "error": "null"})


# PUT /task/:id
@app.route("/api/v1.0/task/<int:id>", methods=["PUT"])
def api_task_update(id):
    # Logic to update a specific task by ID
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # Process the data (e.g., access values):
    name = data.get("name")

    # TODO: And add the new record to a db

    # Return the data
    return jsonify({"id": f"{id}", "success": "true", "error": "null"})
