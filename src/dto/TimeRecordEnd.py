from datetime import datetime
from dto.TimePart import TimePartDto
from dto.TimeRecordBaseDto import TimeRecordBaseDto


class TimeRecordEndDto(TimeRecordBaseDto):
    end_at_date: datetime | None
    end_at_time: str | None

    def __init__(
        self,
        notes: str | None,
        task_id: str | None,
        project_id: str | None,
        end_at_date: datetime | None,
        end_at_time: str | None,
    ):
        super().__init__(None, notes, task_id, project_id)
        self.end_at_date = end_at_date
        self.end_at_time = end_at_time

    def __init__(
        self,
        id: str | None,
        notes: str | None,
        task_id: str | None,
        project_id: str | None,
        end_at_date: datetime | None,
        end_at_time: str | None,
    ):
        super().__init__(id, notes, task_id, project_id)
        self.end_at_date = end_at_date
        self.end_at_time = end_at_time

    def parseJson(raw: any, theId: str | None = None):
        end_at_date = raw.get("end_at_date")
        end_at_time = raw.get("end_at_time")
        notes = raw.get("notes")
        task_id = raw.get("task_id")
        project_id = raw.get("project_id")

        return TimeRecordEndDto(
            theId,
            notes,
            task_id,
            project_id,
            end_at_date,
            end_at_time,
        )
