from datetime import datetime
from uuid import uuid4
from typing import Optional
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


class Project(Model):
    __tablename__ = "boosted_web_project"

    # BTW: init=False means don't make this column part of the constructor
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    color: Mapped[str] = mapped_column(
        nullable=False, doc="The HTML color code (e.g. #000000)"
    )
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=uuid4,
        doc="value is UUIDv4 generated in the Python code",
    )
    isArchived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        default=None, onupdate=datetime.utcnow()
    )

    task = Relationship("Task", back_populates="project", passive_deletes=True)
    time_record = Relationship(
        "TimeRecord", back_populates="project", passive_deletes=True
    )

    # For debugging
    def __repr__(self):
        return f"{self.__class_.__name__}, name: {self.name}"


class Task(Model):
    __tablename__ = "boosted_web_task"
    name: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[str] = mapped_column(
        ForeignKey("boosted_web_project.id", ondelete="CASCADE")
    )
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        default=None, onupdate=datetime.utcnow()
    )

    project = Relationship("Project", back_populates="task")
    time_record = Relationship(
        "TimeRecord", back_populates="task", passive_deletes=True
    )

    # For debugging
    def __repr__(self):
        return f"{self.__class_.__name__}, name: {self.name}"


class TimeRecord(Model):
    __tablename__ = "boosted_web_time_record"
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
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        default=None, onupdate=datetime.utcnow()
    )

    task = Relationship("Task", back_populates="time_record")
    project = Relationship("Project", back_populates="time_record")

    # For debugging
    def __repr__(self):
        return f"{self.__class_.__name__}, name: {self.id}"
