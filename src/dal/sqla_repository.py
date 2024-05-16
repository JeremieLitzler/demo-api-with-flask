from sqlalchemy.orm import scoped_session
from typing import List, TypeVar

from app import app
from interfaces import IRepository

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

    def add(self, item) -> T:
        self._session_db.add(item)
        self._commit()
        self._session_db.refresh(item)
        return item

    def update(self):
        self._commit()

    def delete(self, id):
        item = self.fetch_one(id)
        if item is None:
            return False

        self._session_db.delete(item)
        self._commit()
        return True
