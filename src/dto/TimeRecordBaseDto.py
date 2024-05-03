from datetime import datetime
from dto.TimePart import TimePartDto


class TimeRecordBaseDto:
    id: str | None
    notes: str | None

    task_id: str | None
    project_id: str | None
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        task_id: str | None,
        project_id: str | None,
        notes: str | None,
    ):
        self.id = None  # This will be assigned during task creation
        self.task_id = task_id
        self.project_id = project_id
        self.notes = notes

    def __init__(
        self,
        id: str | None,
        task_id: str | None,
        project_id: str | None,
        notes: str | None,
    ):
        self.id = id
        self.task_id = task_id
        self.project_id = project_id
        self.notes = notes
