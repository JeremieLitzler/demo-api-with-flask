from datetime import datetime
from dto.TimePart import TimePartDto
from dto.TimeRecordBaseDto import TimeRecordBaseDto


class TimeRecordEndDto(TimeRecordBaseDto):
    endAtDate: datetime | None
    endAtTime: str | None

    def __init__(
        self,
        notes: str | None,
        task_id: str | None,
        project_id: str | None,
        endAtDate: datetime | None,
        endAtTime: str | None,
    ):
        super().__init__(None, notes, task_id, project_id)
        self.endAtDate = endAtDate
        self.endAtTime = endAtTime

    def __init__(
        self,
        id: str | None,
        notes: str | None,
        task_id: str | None,
        project_id: str | None,
        endAtDate: datetime | None,
        endAtTime: str | None,
    ):
        super().__init__(id, notes, task_id, project_id)
        self.endAtDate = endAtDate
        self.endAtTime = endAtTime

    def parseJson(raw: any, theId: str | None = None):
        endAtDate = raw.get("endAtDate")
        endAtTime = raw.get("endAtTime")
        notes = raw.get("notes")
        task_id = raw.get("task_id")
        project_id = raw.get("project_id")

        return TimeRecordEndDto(
            theId,
            notes,
            task_id,
            project_id,
            endAtDate,
            endAtTime,
        )
