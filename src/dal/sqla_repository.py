from sqlalchemy.orm import scoped_session
from sqlalchemy.sql.expression import literal_column, bindparam, text
from sqlalchemy.types import String

from typing import List, TypeVar

from app import app
from interfaces import IRepository
from constants.sql_alchemy_result_quantity import SQLAlchemyResultQuantity

T = TypeVar("T")


class SQLAlchemyRepository:

    _model: T = None
    _session_db: scoped_session = NotImplementedError

    def __init__(self, session_db: scoped_session, model: object = None):
        self._session_db = session_db
        self._model = model

    def _check_model(self):
        if self._model is None:
            raise AttributeError("Entity cannot be None. Call `set_model(Model)`")

    def _commit(self):
        self._session_db.commit()

    def set_model(self, model: T):
        self._model = model
        return self

    def fetch_all(self) -> List[T]:
        self._check_model()
        result = self._session_db.query(self._model).all()
        return result

    def fetch_one(self, id) -> T | None:
        self._check_model()
        result = self._session_db.query(self._model).filter(self._model.id == id)
        if result.count() == 1:
            return result.first()
        else:
            return None

    def fetch_one_by_col(self, col_name: str, col_value: str) -> T | None:
        """Beware that the text argument is inserted into the query without any transformation; this may expose you to a SQL Injection vulnerability if you accept values for the text parameter from outside your application. If that's something you need, you'll want to use bindparam, which is about as easy to use; but you will have to invent a name:"""
        """Source: https://stackoverflow.com/a/7546802/3910066"""
        self._check_model()
        search_value = "%{}%".format(col_value)
        search_param = bindparam("filter_value", col_value, String)
        result = (
            self._session_db.query(self._model)
            .filter(text(f"{col_name} like :filter_value").bindparams(search_param))
            .first()
        )

        if result is None:
            return None
        else:
            return result

    def fetch_by_col(
        self,
        col_name: str,
        col_value: str,
        howMany: SQLAlchemyResultQuantity,
        exactly: bool = False,
    ) -> T | list[T] | None:
        """Beware that the text argument is inserted into the query without any transformation; this may expose you to a SQL Injection vulnerability if you accept values for the text parameter from outside your application. If that's something you need, you'll want to use bindparam, which is about as easy to use; but you will have to invent a name:"""
        """Source: https://stackoverflow.com/a/7546802/3910066"""
        self._check_model()
        search_value = "%{}%".format(col_value)
        operator = "like"
        if exactly:
            search_value = "{}".format(col_value)
            operator = "="

        search_param = bindparam("filter_value", col_value, String)
        result = self._session_db.query(self._model).filter(
            text(f"{col_name} {operator} :filter_value").bindparams(search_param)
        )

        if result is None:
            return None

        if howMany == SQLAlchemyResultQuantity.FIRST:
            return result.first()

        if howMany == SQLAlchemyResultQuantity.ALL:
            return result.all()

    def add(self, item) -> T:
        self._session_db.add(item)
        self._commit()
        self._session_db.refresh(item)
        return item

    def update(self, item) -> T:
        self._commit()
        self._session_db.refresh(item)
        return item

    def delete(self, id):
        item = self.fetch_one(id)
        if item is None:
            return False

        self._session_db.delete(item)
        self._commit()
        return True
