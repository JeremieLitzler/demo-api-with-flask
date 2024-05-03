from flask import jsonify, request
from pathlib import Path
import sqlite3
import os
import uuid
import json
from sqlalchemy.orm import scoped_session

from app import app
from utils.api_utils import get_response_json
from dto.TimeRecordStartDto import TimeRecordStartDto
from dto.TimeRecordEndDto import TimeRecordEndDto
from dao.models import TimeRecord
import dal.dal_time_record as dal_time_record
import dal.dal_project as dal_project
import dal.dal_task as dal_task
import services.service_project as service_project
import services.service_time_record as service_time_record
from utils.validators import (
    validate_time_format,
    validate_date_format,
)
from utils.parsers import extract_time_values, convert_str_datetime


def validate_creation_data(data: TimeRecordStartDto, checkProject=True, checkTask=True):
    result = validate_date_format(data.startAtDate)
    if result is False:
        return get_response_json(
            data.id, False, "start date is not format in YYYY-MM-DD", 400
        )

    result = validate_time_format(data.startAtTime)
    if result is False:
        return get_response_json(
            data.id, False, "start time is not format in HH:mm:ss", 400
        )

    task_or_project_specified = (
        data.task_id is not None and data.task_id.strip() != ""
    ) or (data.project_id is not None and data.project_id.strip() != "")
    if task_or_project_specified == False:
        return get_response_json(
            data.id, False, "You need to provide a task or a project", 400
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
        return get_response_json(
            data.id, False, "You need to provide an existing task or project", 404
        )

    return None


def validate_stopping_data(data: TimeRecordEndDto):
    result = validate_date_format(data.endAtDate)
    if result is False:
        return get_response_json(
            data.id, False, "end date is not format in YYYY-MM-DD", 400
        )

    result = validate_time_format(data.endAtTime)
    if result is False:
        return get_response_json(
            data.id, False, "end time is not format in HH:mm:ss", 400
        )


def extract_start_time_values(dto: TimeRecordStartDto, record: TimeRecord):
    start_hours, start_minutes, start_seconds = extract_time_values(dto.startAtTime)
    record.startAtHourTime = start_hours
    record.startAtMinuteTime = start_minutes
    record.startAtSecondTime = start_seconds


def extract_end_time_values(dto: TimeRecordEndDto, record: TimeRecord):
    end_hours, end_minutes, end_seconds = extract_time_values(dto.endAtTime)
    record.endAtHourTime = end_hours
    record.endAtMinuteTime = end_minutes
    record.endAtSecondTime = end_seconds


def sanitize_id(id: str):
    return id.strip() if id is not None else ""


def start(data: TimeRecordStartDto) -> None:

    result = validate_creation_data(data)
    if result is not None:
        return result

    try:
        # TODO: Feat > automap the Dto to Model
        newRecord = TimeRecord()
        newRecord.startAtDate = convert_str_datetime(data.startAtDate)
        newRecord.task_id = data.task_id
        newRecord.project_id = data.project_id
        extract_start_time_values(data, newRecord)

        if data.notes is not None:
            newRecord.notes = data.notes.strip()

        dal_time_record.add(newRecord)

        # Return True if at least one row was added
        message = "null" if True else "No record affected"
        return get_response_json(newRecord.id, True, message)
    except Exception as ex:
        print(ex)
        return get_response_json(id, False, ex)
    finally:
        print("finished calling service_time_record.create")


def get_one(id: str, noJson=False):
    clean_id = sanitize_id(id)
    if clean_id == "":
        return get_response_json(clean_id, False, "ID is required", 400)

    try:
        record = dal_time_record.fetch_by("id", clean_id)

        if record is None:
            return get_response_json(clean_id, False, "Record not found", 404)
        else:
            return jsonify(record)
    except Exception as ex:
        print(ex)
        return get_response_json(clean_id, False, ex, 500)
    finally:
        print("finished calling service_time_record.get_one")


def get_by_task(task_id: str) -> list[TimeRecord]:
    clean_task_id = sanitize_id(task_id)
    try:
        records = dal_time_record.fetch_by("task_id", clean_task_id)
        return jsonify(records)
    except Exception as ex:
        print(ex)
        return get_response_json(clean_task_id, False, ex)
    finally:
        print("finished calling service_time_record.get_by_task")


def get_by_project(project_id: str) -> list[TimeRecord]:
    clean_project_id = sanitize_id(project_id)
    try:
        records = dal_time_record.fetch_by("project_id", clean_project_id)
        return jsonify(records)
    except Exception as ex:
        print(ex)
        return get_response_json(clean_project_id, False, ex)
    finally:
        print("finished calling service_time_record.get_by_project")


def stop(id: str, data: TimeRecordEndDto) -> None:
    clean_id = sanitize_id(id)
    result = validate_stopping_data(data)
    if result is not None:
        return result

    try:
        record = dal_time_record.fetch_by("id", clean_id)
        if record is None:
            return get_response_json(clean_id, False, "Record not found", 404)

        extract_end_time_values(data, record)

        dal_time_record.save()

        return jsonify(record)
    except Exception as ex:
        print(ex)
        return get_response_json(clean_id, False, ex)
    finally:
        print("finished calling service_time_record.update")


def update_notes(id: str, notes: str) -> None:
    clean_id = sanitize_id(id)
    try:
        record = dal_time_record.fetch_by("id", clean_id)
        if record is None:
            return get_response_json(clean_id, False, "Record not found", 404)
        if notes is not None:
            record.notes = notes.strip()

        dal_time_record.save()

        return jsonify(record)
    except Exception as ex:
        print(ex)
        return get_response_json(clean_id, False, ex)
    finally:
        print("finished calling service_time_record.update")


# TODO > Feat: cannot delete a task if records exist for the task
def delete(id: str) -> bool:
    clean_id = id.strip() if id is not None else ""
    if clean_id == "":
        return get_response_json(clean_id, False, "ID is required", 400)

    try:
        result = dal_time_record.delete(clean_id)
        message = "Task deleted successfully" if result else "No record affected"
        return get_response_json(clean_id, True, message)
    except Exception as ex:
        print(ex)
        return get_response_json(clean_id, False, ex)
    finally:
        print("finished calling service_time_record.delete")
