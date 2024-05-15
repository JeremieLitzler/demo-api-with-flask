from datetime import datetime
from dto.TimePart import TimePartDto
from api_swagger import api
from flask_restx import fields

TimeRecordRequestSwaggerModel = api.model(
    "TimeRecord",
    {
        "id": fields.String(readonly=True, description="The record unique identifier"),
        "notes": fields.String(description="The record´s name"),
        "project_id": fields.String(
            description="The project´s ID",
        ),
        "task_id": fields.String(
            description="The task´s ID",
        ),
        "startAtDate": fields.DateTime(
            description="The date on which the record started"
        ),
        "startAtTime": fields.DateTime(
            description="The time at which the record started"
        ),
        "endAtDate": fields.DateTime(description="The date on which the record ended"),
        "endAtTime": fields.DateTime(description="The time at which the record ended"),
        "created_at": fields.DateTime(
            description="The date and time of creation of the record"
        ),
        "updated_at": fields.DateTime(
            description="The date and time of last record´s update"
        ),
    },
)

TimeRecordResponseSwaggerModel = api.model(
    "TimeRecord",
    {
        "id": fields.String(description="The record unique identifier"),
        "notes": fields.String(description="The record´s name"),
        "project_id": fields.String(
            description="The project´s ID",
        ),
        "task_id": fields.String(
            description="The task´s ID",
        ),
        "startAtDate": fields.DateTime(
            description="The date on which the record started"
        ),
        "startAtHourTime": fields.Integer(
            description="The hour of the time at which the record started"
        ),
        "startAtMinuteTime": fields.Integer(
            description="The minute of the time at which the record started"
        ),
        "startAtSecondTime": fields.Integer(
            description="The second of the time at which the record started"
        ),
        "endAtDate": fields.DateTime(description="The date on which the record ended"),
        "endAtHourTime": fields.Integer(
            description="The hour of the time at which the record ended"
        ),
        "endAtMinuteTime": fields.Integer(
            description="The minute of the time at which the record ended"
        ),
        "endAtSecondTime": fields.Integer(
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
