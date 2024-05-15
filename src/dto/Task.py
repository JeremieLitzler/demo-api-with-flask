from datetime import datetime
from api_swagger import api
from flask_restx import fields

TaskSwaggerModel = api.model(
    "Task",
    {
        "id": fields.String(readonly=True, description="The project unique identifier"),
        "name": fields.String(required=True, description="The task´s name"),
        "project_id": fields.String(
            required=True,
            description="The project´s ID",
        ),
        "completed": fields.Boolean(
            default=False,
            description="Flag indicating if the task is completed or not.",
        ),
        "created_at": fields.DateTime(
            description="The date and time of creation of the project"
        ),
        "updated_at": fields.DateTime(
            description="The date and time of last project´s update"
        ),
    },
)


class TaskDto:
    id: str | None
    name: str
    project_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    def __init__(self, name: str, project_id: str, completed: bool = False):
        self.id = None  # This will be assigned during task creation
        self.name = name
        self.project_id = project_id
        self.completed = completed

    def __init__(
        self, name: str, project_id: str, completed: bool = False, id: str | None = None
    ):
        self.id = id  # This will be assigned during task creation
        self.name = name
        self.project_id = project_id
        self.completed = completed

    def parseJson(raw: any, theId: str | None = None):
        name = raw.get("name")
        project_id = raw.get("project_id")
        completed = raw.get("completed")
        return TaskDto(name, project_id, completed, theId)
