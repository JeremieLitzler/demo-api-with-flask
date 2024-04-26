# Thanks to https://stackoverflow.com/a/57732785/3910066
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Optional
from sqlalchemy import func
from sqlalchemy import ForeignKey, Column, DateTime, String, Boolean
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    mapped_column,
    Relationship,
)


# Define base class for models
class Model(MappedAsDataclass, DeclarativeBase):
    pass


# Required to be able to serialize the model to JSON
@dataclass
class Project(Model):
    __tablename__ = "boosted_web_project"

    # BTW: init=False means don't make this column part of the constructor
    id: Mapped[str] = mapped_column(
        primary_key=True,
        doc="value is UUIDv4 generated in the Python code",
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    color: Mapped[str] = mapped_column(
        nullable=False, doc="The HTML color code (e.g. #000000)"
    )
    # Use func.now from sqlalchemy and server_default otherwise the timestamp
    # will be off
    # TODO: Feat > format date to YYYY-MM-DD hh:mm:ss
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    # Same for onupdate, use func.now
    # TODO: Feat > format date to YYYY-MM-DD hh:mm:ss
    updated_at: Mapped[datetime] = mapped_column(
        init=False, nullable=True, onupdate=func.now()
    )
    is_archived: Mapped[bool] = mapped_column(default=False)

    task = Relationship("Task", back_populates="project", passive_deletes=True)
    time_record = Relationship(
        "TimeRecord", back_populates="project", passive_deletes=True
    )

    def __init__(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = uuid4().hex
        super().__init__(**kwargs)

    # For debugging
    def __repr__(self):
        return f"{self.__class_.__name__}, name: {self.name}"


class Task(Model):
    __tablename__ = "boosted_web_task"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("boosted_web_project.id", ondelete="CASCADE")
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True, onupdate=datetime.utcnow()
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    project = Relationship("Project", back_populates="task")
    time_record = Relationship(
        "TimeRecord", back_populates="task", passive_deletes=True
    )

    def __init__(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = uuid4().hex
        super().__init__(**kwargs)

    # For debugging
    def __repr__(self):
        return f"{self.__class_.__name__}, name: {self.name}"


class TimeRecord(Model):
    __tablename__ = "boosted_web_time_record"
    id: Mapped[str] = mapped_column(primary_key=True)
    startAtHourTime: Mapped[int]
    startAtMinuteTime: Mapped[int]
    startAtSecondTime: Mapped[int]
    startAtDate: Mapped[datetime] = mapped_column(
        doc="The date (year-month-day) the record was started"
    )
    endAtHourTime: Mapped[int]
    endAtMinuteTime: Mapped[int]
    endAtSecondTime: Mapped[int]
    endAtDate: Mapped[datetime] = mapped_column(
        doc="The date (year-month-day) the record was stopped"
    )
    notes: Mapped[str]
    project_id: Mapped[str] = mapped_column(
        ForeignKey("boosted_web_project.id", ondelete="CASCADE"), nullable=True
    )
    task_id: Mapped[str] = mapped_column(
        ForeignKey("boosted_web_task.id", ondelete="CASCADE"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True, onupdate=datetime.utcnow()
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    task = Relationship("Task", back_populates="time_record")
    project = Relationship("Project", back_populates="time_record")

    def __init__(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = uuid4()
        super().__init__(**kwargs)

    # For debugging
    def __repr__(self):
        return f"{self.__class_.__name__}, name: {self.id}"
