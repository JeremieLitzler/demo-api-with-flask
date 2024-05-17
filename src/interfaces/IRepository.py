from abc import ABC, abstractmethod
from typing import TypeVar
from constants.sql_alchemy_result_quantity import SQLAlchemyResultQuantity

T = TypeVar("T")


class IRepository(ABC):
    @abstractmethod
    def set_model(self, model: T):
        raise NotImplementedError

    @abstractmethod
    def fetch_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def fetch_one(self, id) -> T:
        raise NotImplementedError

    @abstractmethod
    def fetch_one_by_col(self, col_name: str, col_value: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def fetch_by_col(
        self, col_name: str, col_value: str, howMany: SQLAlchemyResultQuantity
    ) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, item: T):
        raise NotImplementedError

    @abstractmethod
    def update(self, item: T):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError
