from flask import jsonify, request
from pathlib import Path
import sqlite3
import os
import uuid
import json
from sqlalchemy.orm import scoped_session

from app import app
from utils.api_utils import get_response_json, raise_business_error, handle_ex
from dto.TimeRecord import TimeRecordStartDto, TimeRecordEndDto
from dao.models import TimeRecord
import dal.dal_time_record as dal_time_record
import dal.dal_project as dal_project
import dal.dal_task as dal_task
import services.service_project as service_project
import services.service_record as service_record
from utils.validators import (
    validate_time_format,
    validate_date_format,
)
from utils.parsers import extract_time_values, convert_str_date, convert_str_datetime


def validate_creation_data(data: TimeRecordStartDto, checkParent=True):
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
        task = dal_task.fetch_one(sanitize_id(data.task_id))
        task_exists = True if task is not None else False

    project_exists = False
    if data.project_id is not None and data.project_id.strip() != "":
        project = dal_project.fetch_one(sanitize_id(data.project_id))
        project_exists = True if project is not None else False

    if task_exists is False and project_exists is False:
        raise_business_error(
            data.id, False, "You need to provide an existing task or project", 404
        )


def validate_stopping_data(data: TimeRecordEndDto):
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
        raise_business_error(data.id, False, "end time is not format in HH:mm:ss", 422)


def extract_start_time_values(dto: TimeRecordStartDto, record: TimeRecord):
    start_hours, start_minutes, start_seconds = extract_time_values(dto.start_at_time)
    record.start_at_hour_time = start_hours
    record.start_at_minute_time = start_minutes
    record.start_at_second_time = start_seconds


def extract_end_time_values(dto: TimeRecordEndDto, record: TimeRecord):
    end_hours, end_minutes, end_seconds = extract_time_values(dto.end_at_time)
    record.end_at_hour_time = end_hours
    record.end_at_minute_time = end_minutes
    record.end_at_second_time = end_seconds


def sanitize_id(id: str):
    return id.strip() if id is not None else ""


def start(jsonData: dict) -> None:
    try:
        data = TimeRecordStartDto.parseJson(jsonData)
        validate_creation_data(data)
        # TODO: Feat > automap the Dto to Model
        new_record = TimeRecord()
        new_record.start_at_date = convert_str_date(data.start_at_date)
        new_record.task_id = data.task_id
        new_record.project_id = data.project_id
        extract_start_time_values(data, new_record)

        if data.notes is not None:
            new_record.notes = data.notes.strip()

        inserted_record = dal_time_record.add(new_record)
        return inserted_record, 201
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.create")


def get_one(id: str, noJson=False):
    try:
        clean_id = sanitize_id(id)
        if clean_id == "":
            raise_business_error(clean_id, False, "ID is required", 422)

        record = dal_time_record.fetch_by("id", clean_id)

        if noJson:
            return record
        if record is None:
            raise_business_error(id, False, "Record not found", 404)

        return record
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.get_one")


def get_by_task(task_id: str) -> list[TimeRecord]:
    clean_task_id = sanitize_id(task_id)
    try:
        records = dal_time_record.fetch_by("task_id", clean_task_id)
        return records
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.get_by_task")


def get_by_project(project_id: str) -> list[TimeRecord]:
    clean_project_id = sanitize_id(project_id)
    try:
        records = dal_time_record.fetch_by("project_id", clean_project_id)
        return records
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.get_by_project")


def end_strickly_greater_than_start(
    startDto: TimeRecordStartDto, endDto: TimeRecordEndDto
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


def update_one(id: str, jsonData: dict):
    try:
        clean_id = sanitize_id(id)
        record = dal_time_record.fetch_by("id", clean_id)
        if record is None:
            raise_business_error(clean_id, False, "Record not found", 404)

        notes = jsonData.get("notes", None)

        endDto = TimeRecordEndDto.parseJson(jsonData, id)
        result = validate_stopping_data(endDto)
        if result is not None:
            return result

        startDto = TimeRecordStartDto.parseJson(jsonData, id)
        result = validate_creation_data(startDto, checkParent=False)
        if result is not None:
            return result

        result = end_strickly_greater_than_start(startDto, endDto)
        if result is not None:
            return result

        record.start_at_date = convert_str_date(startDto.start_at_date)
        extract_start_time_values(startDto, record)
        record.end_at_date = convert_str_date(endDto.end_at_date)
        extract_end_time_values(endDto, record)
        if notes is not None:
            record.notes = notes.strip()

        dal_time_record.save()

        return record
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.update")


def stop(id: str, jsonData: dict) -> None:
    clean_id = sanitize_id(id)
    try:
        record = dal_time_record.fetch_by("id", clean_id)
        if record is None:
            raise_business_error(clean_id, False, "Record not found", 404)

        data = TimeRecordEndDto.parseJson(jsonData, id)
        result = validate_stopping_data(data)
        if result is not None:
            return result

        record.end_at_date = convert_str_date(data.end_at_date)
        extract_end_time_values(data, record)

        dal_time_record.save()
        return record
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.stop")


def update_notes(id: str, jsonData: dict) -> None:
    clean_id = sanitize_id(id)
    try:
        record = dal_time_record.fetch_by("id", clean_id)
        if record is None:
            raise_business_error(clean_id, False, "Record not found", 404)

        notes = jsonData.get("notes", None)
        if notes is not None:
            record.notes = notes.strip()

        dal_time_record.save()

        return record
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.update_notes")


# TODO > Feat: cannot delete a task if records exist for the task
def delete_one(id: str) -> bool:
    if id.strip() == "":
        raise_business_error(id, False, "ID is required", 422)

    try:
        result = dal_time_record.delete(id)
        return "", 204
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.delete")
