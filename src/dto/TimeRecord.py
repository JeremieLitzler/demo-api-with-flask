from datetime import datetime
from dto.TimePart import TimePartDto
from api_swagger import api
from flask_restx import fields

RecordStartRequestSwaggerModel = api.model(
    "RecordStartRequest",
    {
        "notes": fields.String(description="The record´s notes"),
        "project_id": fields.String(
            description="The project´s ID",
        ),
        "task_id": fields.String(
            description="The task´s ID",
        ),
        "start_at_date": fields.DateTime(
            description="The date on which the record started. Format expected to be a valid (e.g. 2024-05-15)."
        ),
        "start_at_time": fields.DateTime(
            description="The time at which the record started. Format expected to be a valid (e.g. 18:00:00)."
        ),
    },
)
RecordStopRequestSwaggerModel = api.model(
    "RecordStopRequest",
    {
        "id": fields.String(readonly=True, description="The record unique identifier"),
        "notes": fields.String(description="The record´s notes"),
        "project_id": fields.String(
            description="The project´s ID",
        ),
        "task_id": fields.String(
            description="The task´s ID",
        ),
        "end_at_date": fields.DateTime(
            description="The date on which the record ended. Format expected to be a valid (e.g. 2024-05-15)."
        ),
        "end_at_time": fields.DateTime(
            description="The time at which the record ended. Format expected to be a valid (e.g. 18:00:00)."
        ),
    },
)
RecordUpdateRequestSwaggerModel = api.model(
    "RecordUpdateRequest",
    {
        "id": fields.String(readonly=True, description="The record unique identifier"),
        "notes": fields.String(description="The record´s notes"),
        "project_id": fields.String(
            description="The project´s ID",
        ),
        "task_id": fields.String(
            description="The task´s ID",
        ),
        "start_at_date": fields.DateTime(
            description="The date on which the record started. Format expected to be a valid (e.g. 2024-05-15)."
        ),
        "start_at_time": fields.DateTime(
            description="The time at which the record started. Format expected to be a valid (e.g. 18:00:00)."
        ),
        "end_at_date": fields.DateTime(
            description="The date on which the record ended. Format expected to be a valid (e.g. 2024-05-15)."
        ),
        "end_at_time": fields.DateTime(
            description="The time at which the record ended. Format expected to be a valid (e.g. 18:00:00)."
        ),
    },
)
RecordNotesRequestSwaggerModel = api.model(
    "RecordNotesRequest",
    {
        "id": fields.String(readonly=True, description="The record unique identifier"),
        "notes": fields.String(description="The record´s notes"),
    },
)
RecordResponseSwaggerModel = api.model(
    "RecordResponse",
    {
        "id": fields.String(description="The record unique identifier"),
        "notes": fields.String(description="The record´s notes"),
        "project_id": fields.String(
            description="The project´s ID",
        ),
        "task_id": fields.String(
            description="The task´s ID",
        ),
        "start_at_date": fields.DateTime(
            description="The date on which the record started"
        ),
        "start_at_hour_time": fields.Integer(
            description="The hour of the time at which the record started"
        ),
        "start_at_minute_time": fields.Integer(
            description="The minute of the time at which the record started"
        ),
        "start_at_second_time": fields.Integer(
            description="The second of the time at which the record started"
        ),
        "end_at_date": fields.DateTime(
            description="The date on which the record ended"
        ),
        "end_at_hour_time": fields.Integer(
            description="The hour of the time at which the record ended"
        ),
        "end_at_minute_time": fields.Integer(
            description="The minute of the time at which the record ended"
        ),
        "end_at_second_time": fields.Integer(
            description="The second of the time at which the record ended"
        ),
        "created_at": fields.DateTime(
            description="The date and time of creation of the record"
        ),
        "updated_at": fields.DateTime(
            description="The date and time of last record´s update"
        ),
    },
)


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
