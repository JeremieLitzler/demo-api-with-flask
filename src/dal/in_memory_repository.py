from interfaces import IRepository


class InMemoryRepository(IRepository):
    def __init__(self):
        self._data_source = []

    def get_all(self):
        return self._data_source

    def get_by_id(self, id):
        return next((item for item in self._data_source if item["id"] == id), None)

    def create(self, item):
        item["id"] = len(self._data_source) + 1
        self._data_source.append(item)
        return item

    def update(self, item):
        index = next(
            (i for i, obj in enumerate(self._data_source) if obj["id"] == item["id"]),
            None,
        )
        if index is not None:
            self._data_source[index] = item
            return True
        return False

    def delete(self, id):
        index = next(
            (i for i, obj in enumerate(self._data_source) if obj["id"] == id), None
        )
        if index is not None:
            self._data_source.pop(index)
            return True
        return False
