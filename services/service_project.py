from flask import jsonify, request
from pathlib import Path

import threading
import os
import json
import uuid
from utils.validators import validate_required_properties
from utils.json_utils import toJSON

from dto.ProjectData import ProjectData

def create_project(project_data: ProjectData):
  required_properties = ["name", "color"]
  validation_error = validate_required_properties(project_data, required_properties)
  if validation_error:
    return jsonify(validation_error), 400

  # Generate unique project ID (e.g., using uuid)
  project_id = str(uuid.uuid4())
  project_data.id = project_id  # Assign ID to the object

  # Build file path with project ID
  # No need to explicitly create the "projects" folder: 
  #     Python's open function will automatically create any missing 
  #     directories in the path if they don't already exist.

  # See https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir
  # Create the "projects" dir if not exists, 
  # Otherwise it doesn't do anything thanks to exist_ok=True
  Path(f"db{os.sep}projects").mkdir(parents=True, exist_ok=True)
  project_file = os.path.join(f"db{os.sep}projects", f"{project_id}.json")

  # Check if file already exists
  if os.path.exists(project_file):
      return jsonify({"error": "Project with this ID already exists"}), 409

  # Create a lock object to synchronize file access
  lock = threading.Lock()

  # Try creating the file with exclusive access to avoid race conditions
  try:
    if lock.acquire(blocking=True):  # Wait until lock is acquired
      try:
        with open(project_file, "w") as f:
          json.dump(toJSON(project_data), f)
        return jsonify({"message": "Project created successfully", "id": project_id}), 201
      finally:
        lock.release()  # Ensure lock is released even on exceptions
  except OSError as e:
      # Handle file system error (e.g., disk full)
      return jsonify({"error": f"Error creating project file: {str(e)}"}), 500
