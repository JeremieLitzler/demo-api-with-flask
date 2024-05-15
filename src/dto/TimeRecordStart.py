from datetime import datetime
from dto.TimeRecordBaseDto import TimeRecordBaseDto


class TimeRecordStartDto(TimeRecordBaseDto):
    start_at_date: datetime | None
    start_at_time: str | None

    def __init__(
        self,
        id: str | None,
        task_id: str | None,
        project_id: str | None,
        notes: str | None,
        start_at_date: datetime | None,
        start_at_time: str | None,
    ):
        super().__init__(id, task_id, project_id, notes)
        self.start_at_date = start_at_date
        self.start_at_time = start_at_time

    def parseJson(raw: any, theId: str | None = None):
        start_at_date = raw.get("start_at_date")
        start_at_time = raw.get("start_at_time")
        notes = raw.get("notes")
        task_id = raw.get("taskId")
        project_id = raw.get("projectId")

        return TimeRecordStartDto(
            theId,
            task_id,
            project_id,
            notes,
            start_at_date,
            start_at_time,
        )
