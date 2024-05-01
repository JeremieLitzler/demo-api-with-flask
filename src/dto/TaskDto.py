from datetime import datetime


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
