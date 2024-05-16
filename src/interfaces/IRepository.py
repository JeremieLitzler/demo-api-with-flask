from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class IRepository(ABC):
    @abstractmethod
    def set_model(model: T):
        raise NotImplementedError

    @abstractmethod
    def fetch_all(self):
        raise NotImplementedError

    @abstractmethod
    def fetch_one(self, id):
        raise NotImplementedError

    @abstractmethod
    def add(self, item):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError
