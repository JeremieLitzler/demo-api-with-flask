from flask import jsonify, request
from pathlib import Path
import sqlite3
import os
import uuid

from dto.ProjectDto import ProjectDto
from utils.validators import validate_required_properties
from utils.reflection import get_tuple_from_type
import dal.dal_project as dal_project
from dal.models import Project


def get_response_json(id: int, success: bool, message: str = "null"):
    return jsonify({"id": f"{id}", "success": f"{success}", "message": f"{message}"})


def create_project(project_data: ProjectDto) -> None:

    try:
        # Replace 'project_data.db' with your desired database filename
        newProject = Project(name=project_data.name, color=project_data.color)
        dal_project.add(newProject)

        # Return True if at least one row was added
        message = "null" if True else "No record affected"
        return get_response_json(newProject.id, True, message)
    except Exception as ex:
        return get_response_json("", False, ex.with_traceback)


def get_project(project_id: str) -> ProjectDto:
    try:
        conn = sqlite3.connect(f"db{os.sep}database_sqllite3.db")
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, name, color, isArchived FROM projects WHERE id = ?""",
            (project_id,),
        )
        project_data = cursor.fetchone()
        ProjectRecord = get_tuple_from_type(
            ProjectDto
        )  # Get namedtuple type dynamically

        if project_data:
            project = ProjectRecord(*project_data)
            return jsonify(project._asdict())
        else:
            return jsonify({"message": "Project not found"}), 404

    finally:
        conn.close()


def get_projects() -> list[ProjectDto]:
    try:
        projects = dal_project.fetchAll()

        ProjectRecord = get_tuple_from_type(
            ProjectDto
        )  # Get namedtuple type dynamically

        projects = []
        for record in projects:
            projects.append(
                ProjectRecord(*record)
            )  # Unpack data using * operator for each row
        return projects
    finally:
        print("finished calling get_projects")


def update_project(project_data: ProjectDto) -> None:
    try:
        conn = sqlite3.connect(f"db{os.sep}database_sqllite3.db")
        cursor = conn.cursor()
        # Get attribute names with non-None values
        attrs_to_update = [
            attr
            for attr in vars(project_data).keys()
            if vars(project_data)[attr] is not None
        ]

        # Build the SET clause dynamically based on non-None attributes
        set_clause = ", ".join([f"{attr} = ?" for attr in attrs_to_update])

        # Prepare the update query with placeholders for non-None values
        update_query = f"UPDATE projects SET {set_clause} WHERE id = ?"

        # Extract values from the project_data object based on the selected attributes
        values = [getattr(project_data, attr) for attr in attrs_to_update]
        values.append(project_data.id)  # Add ID for WHERE clause

        # Execute the update query with filtered values
        cursor.execute(update_query, values)

        conn.commit()

        # Retrieve the updated data using get_project (assuming it exists)
        project = get_project(project_data.id)

        if project:
            return project
        else:
            return jsonify({"message": "Project not found"}), 404

    finally:
        conn.close()


def delete_project(id: str) -> bool:
    try:
        conn = sqlite3.connect(f"db{os.sep}database_sqllite3.db")
        cursor = conn.cursor()

        query = f"DELETE FROM projects WHERE id = ?"
        cursor.execute(query, (id,))
        conn.commit()

        # Check if any rows were affected (i.e., if a project was deleted)
        rows_affected = cursor.rowcount
        message = "null" if rows_affected > 0 else "No record affected"
        return get_response_json(id, rows_affected > 0, message)

    finally:
        conn.close()
