from datetime import datetime
from dto.TimeRecordBaseDto import TimeRecordBaseDto


class TimeRecordStartDto(TimeRecordBaseDto):
    startAtDate: datetime | None
    startAtTime: str | None

    def __init__(
        self,
        id: str | None,
        task_id: str | None,
        project_id: str | None,
        notes: str | None,
        startAtDate: datetime | None,
        startAtTime: str | None,
    ):
        super().__init__(id, task_id, project_id, notes)
        self.startAtDate = startAtDate
        self.startAtTime = startAtTime

    def parseJson(raw: any, theId: str | None = None):
        startAtDate = raw.get("startAtDate")
        startAtTime = raw.get("startAtTime")
        notes = raw.get("notes")
        task_id = raw.get("taskId")
        project_id = raw.get("projectId")

        return TimeRecordStartDto(
            theId,
            task_id,
            project_id,
            notes,
            startAtDate,
            startAtTime,
        )
