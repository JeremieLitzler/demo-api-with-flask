from datetime import datetime


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
