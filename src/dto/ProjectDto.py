from datetime import datetime
from api_swagger import api
from flask_restx import fields

project = api.model(
    "Project",
    {
        "id": fields.String(readonly=True, description="The project unique identifier"),
        "name": fields.String(required=True, description="The project´s name"),
        "color": fields.String(
            required=True,
            description='The project´s color code (HTML Hexadecimal code starting with "#")',
        ),
        "is_archived": fields.Boolean(
            default=False,
            description="Flag indicating if the project is archived or not.",
        ),
        "created_at": fields.DateTime(
            description="The date and time of creation of the project"
        ),
        "updated_at": fields.DateTime(
            description="The date and time of last project´s update"
        ),
    },
)


class ProjectDto:
    id: str | None
    name: str
    color: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    def __init__(self, name: str, color: str, is_archived: bool = False):
        self.id = None  # This will be assigned during project creation
        self.name = name
        self.color = color
        self.is_archived = is_archived

    def __init__(
        self, name: str, color: str, is_archived: bool = False, id: str | None = None
    ):
        self.id = id  # This will be assigned during project creation
        self.name = name
        self.color = color
        self.is_archived = is_archived

    def parseJson(raw: any, theId: str | None = None):
        name = raw.get("name")
        color = raw.get("color")
        is_archived = raw.get("is_archived")
        return ProjectDto(name, color, is_archived, theId)
