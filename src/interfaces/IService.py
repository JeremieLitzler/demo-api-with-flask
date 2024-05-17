from abc import ABC, abstractmethod
from typing import TypeVar

from dao.models import Project

T = TypeVar("T")


class IService(ABC):
    @abstractmethod
    def create(self, jsonData: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_one(self, id: str, noJson=False) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def update_one(self, id: str, jsonData: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, id: str):
        raise NotImplementedError
