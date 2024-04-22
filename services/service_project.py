from flask import jsonify, request
from pathlib import Path

import sqlite3
import os
import json
import uuid
from utils.validators import validate_required_properties
from utils.reflection import get_tuple_from_type
from dto.ProjectDto import ProjectDto

def create_project(project_data: ProjectDto) -> None:
  # Replace 'project_data.db' with your desired database filename
  try:
    conn = sqlite3.connect(f'db{os.sep}database_sqllite3.db')
    cursor = conn.cursor()

    project_data.id = str(uuid.uuid4())

    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                      id TEXT PRIMARY KEY,
                      name TEXT NOT NULL,
                      color TEXT NOT NULL,
                      isArchived INTEGER NOT NULL
                    )''')

    # Escape single quotes in data if necessary (see note below)
    name = project_data.name.replace("'", "''")
    color = project_data.color.replace("'", "''")
    is_archived = int(project_data.isArchived)  # Convert bool to int for database

    cursor.execute('''INSERT INTO projects (id, name, color, isArchived)
                      VALUES (?, ?, ?, ?)''',
                    (project_data.id, name, color, is_archived))

    # ... (rest of your code)

    conn.commit()
    return jsonify({'id': f'{project_data.id}', 'success': 'true', 'error': 'null'})
  finally:  
    conn.close()
  
def get_project(project_id: str) -> ProjectDto:
  try:
    conn = sqlite3.connect(f'db{os.sep}database_sqllite3.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, name, color, isArchived FROM projects WHERE id = ?''', (project_id,))
    project_data = cursor.fetchone()
    ProjectRecord = get_tuple_from_type(ProjectDto)  # Get namedtuple type dynamically

    if project_data:
      return ProjectRecord(*project_data)  # Unpack data using * operator
    else:
      return None

  finally:  
    conn.close()
    
def get_projects() -> list[ProjectDto]:
  try:
    conn = sqlite3.connect(f'db{os.sep}database_sqllite3.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT id, name, color, isArchived FROM projects''')
    project_data = cursor.fetchall()

    ProjectRecord = get_tuple_from_type(ProjectDto)  # Get namedtuple type dynamically

    projects = []
    for row in project_data:
      projects.append(ProjectRecord(*row))  # Unpack data using * operator for each row
    return projects
  finally:  
    conn.close()
