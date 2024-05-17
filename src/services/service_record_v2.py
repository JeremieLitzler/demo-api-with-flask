from flask import jsonify, request
from sqlalchemy.orm import scoped_session

from interfaces import IRepository, IService
from constants.sql_alchemy_result_quantity import SQLAlchemyResultQuantity
from utils.api_utils import get_response_json, raise_business_error, handle_ex
from dto.TimeRecord import TimeRecordStartDto, TimeRecordEndDto
from dao.models import TimeRecord
from utils.validators import (
    validate_time_format,
    validate_date_format,
)
from utils.parsers import extract_time_values, convert_str_date, convert_str_datetime


class RecordService:
    _repository: IRepository
    _taskService: IService
    _projectService: IService

    def __init__(
        self,
        repository: IRepository,
        projectService: IService = None,
        taskService: IService = None,
    ):
        self._repository = repository
        self._projectService = projectService
        self._taskService = taskService

    def validate_creation_data(self, data: TimeRecordStartDto, checkParent=True):
        if data.start_at_date is None:
            raise_business_error(data.id, False, "start date is required", 422)

        result = validate_date_format(data.start_at_date)
        if result is False:
            raise_business_error(
                data.id, False, "start date is not format in YYYY-MM-DD", 422
            )

        if data.start_at_time is None:
            raise_business_error(data.id, False, "start time is required", 422)

        result = validate_time_format(data.start_at_time)
        if result is False:
            raise_business_error(
                data.id, False, "start time is not format in HH:mm:ss", 422
            )

        if checkParent is False:
            return None

        task_or_project_specified = (
            data.task_id is not None and data.task_id.strip() != ""
        ) or (data.project_id is not None and data.project_id.strip() != "")
        if task_or_project_specified == False:
            raise_business_error(
                data.id, False, "You need to provide a task or a project", 422
            )

        # TODO > Feat : check project or task exist
        task_exists = False
        if data.task_id is not None and data.task_id.strip() != "":
            task = self._taskService.get_one(self.sanitize_id(data.task_id))
            task_exists = True if task is not None else False

        project_exists = False
        if data.project_id is not None and data.project_id.strip() != "":
            project = self._projectService.get_one(self.sanitize_id(data.project_id))
            project_exists = True if project is not None else False

        if task_exists is False and project_exists is False:
            raise_business_error(
                data.id, False, "You need to provide an existing task or project", 404
            )

    def validate_stopping_data(self, data: TimeRecordEndDto):
        if data.end_at_date is None:
            raise_business_error(data.id, False, "end date is required", 422)

        result = validate_date_format(data.end_at_date)
        if result is False:
            raise_business_error(
                data.id, False, "end date is not format in YYYY-MM-DD", 422
            )

        if data.end_at_time is None:
            raise_business_error(data.id, False, "end time is required", 422)

        result = validate_time_format(data.end_at_time)
        if result is False:
            raise_business_error(
                data.id, False, "end time is not format in HH:mm:ss", 422
            )

    def extract_start_time_values(self, dto: TimeRecordStartDto, record: TimeRecord):
        start_hours, start_minutes, start_seconds = extract_time_values(
            dto.start_at_time
        )
        record.start_at_hour_time = start_hours
        record.start_at_minute_time = start_minutes
        record.start_at_second_time = start_seconds

    def extract_end_time_values(self, dto: TimeRecordEndDto, record: TimeRecord):
        end_hours, end_minutes, end_seconds = extract_time_values(dto.end_at_time)
        record.end_at_hour_time = end_hours
        record.end_at_minute_time = end_minutes
        record.end_at_second_time = end_seconds

    def sanitize_id(self, id: str):
        return id.strip() if id is not None else ""

    def start(self, jsonData: dict) -> None:
        try:
            data = TimeRecordStartDto.parseJson(jsonData)
            self.validate_creation_data(data)
            # TODO: Feat > automap the Dto to Model
            new_record = TimeRecord()
            new_record.start_at_date = convert_str_date(data.start_at_date)
            new_record.task_id = data.task_id
            new_record.project_id = data.project_id
            self.extract_start_time_values(data, new_record)

            if data.notes is not None:
                new_record.notes = data.notes.strip()

            inserted_record = self._repository.add(new_record)
            return inserted_record, 201
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.create")

    def get_one(self, id: str, noJson=False):
        try:
            clean_id = self.sanitize_id(id)
            if clean_id == "":
                raise_business_error(clean_id, False, "ID is required", 422)

            record = self._repository.set_model(TimeRecord).fetch_one(clean_id)

            if noJson:
                return record
            if record is None:
                raise_business_error(id, False, "Record not found", 404)

            return record
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.get_one")

    def get_all(self) -> list[TimeRecord]:
        try:
            records = self._repository.set_model(TimeRecord).fetch_all()
            return records
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling get_all")

    def get_by_task(self, task_id: str) -> list[TimeRecord]:
        clean_task_id = self.sanitize_id(task_id)
        try:
            records = self._repository.set_model(TimeRecord).fetch_by_col(
                "task_id", clean_task_id, SQLAlchemyResultQuantity.ALL, exactly=True
            )
            return records
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.get_by_task")

    def get_by_project(self, project_id: str) -> list[TimeRecord]:
        clean_project_id = self.sanitize_id(project_id)
        try:
            records = self._repository.set_model(TimeRecord).fetch_by_col(
                "project_id",
                clean_project_id,
                SQLAlchemyResultQuantity.ALL,
                exactly=True,
            )
            return records
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.get_by_project")

    def end_strickly_greater_than_start(
        self, startDto: TimeRecordStartDto, endDto: TimeRecordEndDto
    ):
        fullStartDate = convert_str_datetime(
            f"{startDto.start_at_date} {startDto.start_at_time}"
        )
        fullEndDate = convert_str_datetime(f"{endDto.end_at_date} {endDto.end_at_time}")

        if fullStartDate > fullEndDate:
            raise_business_error(
                startDto.id, False, "The record cannot starts after it ends.", 422
            )

        return None

    def update_one(self, id: str, jsonData: dict):
        try:
            clean_id = self.sanitize_id(id)
            record = self._repository.set_model(TimeRecord).fetch_one(clean_id)
            if record is None:
                raise_business_error(clean_id, False, "Record not found", 404)

            notes = jsonData.get("notes", None)

            endDto = TimeRecordEndDto.parseJson(jsonData, id)
            result = self.validate_stopping_data(endDto)
            if result is not None:
                return result

            startDto = TimeRecordStartDto.parseJson(jsonData, id)
            result = self.validate_creation_data(startDto, checkParent=False)
            if result is not None:
                return result

            result = self.end_strickly_greater_than_start(startDto, endDto)
            if result is not None:
                return result

            record.start_at_date = convert_str_date(startDto.start_at_date)
            self.extract_start_time_values(startDto, record)
            record.end_at_date = convert_str_date(endDto.end_at_date)
            self.extract_end_time_values(endDto, record)
            if notes is not None:
                record.notes = notes.strip()

            return self._repository.update(record)
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.update")

    def stop(self, id: str, jsonData: dict) -> None:
        clean_id = self.sanitize_id(id)
        try:
            record = self._repository.set_model(TimeRecord).fetch_one(clean_id)
            if record is None:
                raise_business_error(clean_id, False, "Record not found", 404)

            data = TimeRecordEndDto.parseJson(jsonData, id)
            result = self.validate_stopping_data(data)
            if result is not None:
                return result

            record.end_at_date = convert_str_date(data.end_at_date)
            self.extract_end_time_values(data, record)

            return self._repository.update(record)
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.stop")

    def update_notes(self, id: str, jsonData: dict) -> None:
        clean_id = self.sanitize_id(id)
        try:
            record = self._repository.set_model(TimeRecord).fetch_one(clean_id)
            if record is None:
                raise_business_error(clean_id, False, "Record not found", 404)

            notes = jsonData.get("notes", None)
            if notes is not None:
                record.notes = notes.strip()

            return self._repository.update(record)
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.update_notes")

    # TODO > Feat: cannot delete a task if records exist for the task
    def delete_one(self, id: str) -> bool:
        if id.strip() == "":
            raise_business_error(id, False, "ID is required", 422)

        try:
            result = self._repository.set_model(TimeRecord).delete(id)
            return "", 204
        except Exception as ex:
            print(ex)
            handle_ex(ex)
        finally:
            print("finished calling service_time_record.delete")
