from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
)

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Optional
from sqlalchemy import func
from sqlalchemy import ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import (
    Relationship,
    Mapped,
    mapped_column,
)


# Define base class for models
class Model(MappedAsDataclass, DeclarativeBase):
    pass


# @dataclass is a required decorator to be able to serialize the model to JSON
# Thanks to https://stackoverflow.com/a/57732785/3910066
@dataclass
class Project(Model):
    __tablename__ = "boosted_web_project"

    # BTW: init=False means don't make this column part of the constructor
    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        doc="value is UUIDv4 generated in the Python code",
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    color: Mapped[str] = mapped_column(
        String(7), nullable=False, doc="The HTML color code (e.g. #000000)"
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


@dataclass
class Task(Model):
    __tablename__ = "boosted_web_task"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    completed: Mapped[bool] = mapped_column(nullable=True)
    project_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("boosted_web_project.id", ondelete="CASCADE")
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


# Required to be able to serialize the model to JSON
@dataclass
class TimeRecord(Model):
    __tablename__ = "boosted_web_time_record"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    start_at_hour_time: Mapped[int]
    start_at_minute_time: Mapped[int]
    start_at_second_time: Mapped[int]
    start_at_date: Mapped[datetime] = mapped_column(
        doc="The date (year-month-day) the record was started"
    )
    end_at_hour_time: Mapped[int] = mapped_column(init=False, nullable=True)
    end_at_minute_time: Mapped[int] = mapped_column(init=False, nullable=True)
    end_at_second_time: Mapped[int] = mapped_column(init=False, nullable=True)
    end_at_date: Mapped[datetime] = mapped_column(
        init=False,
        nullable=True,
        doc="The date (year-month-day) the record was stopped",
    )
    notes: Mapped[str] = mapped_column(String(4000), init=False, nullable=True)
    project_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("boosted_web_project.id", ondelete="CASCADE"),
        nullable=True,
    )
    task_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("boosted_web_task.id", ondelete="CASCADE"), nullable=True
    )
    # TODO: Feat > format date to YYYY-MM-DD hh:mm:ss
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    # Same for onupdate, use func.now
    # TODO: Feat > format date to YYYY-MM-DD hh:mm:ss
    updated_at: Mapped[datetime] = mapped_column(
        init=False, nullable=True, onupdate=func.now()
    )

    task = Relationship("Task", back_populates="time_record")
    project = Relationship("Project", back_populates="time_record")

    def __init__(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = uuid4().hex
        super().__init__(**kwargs)

    # For debugging
    def __repr__(self):
        return f"{self.__class_.__name__}, name: {self.id}"
