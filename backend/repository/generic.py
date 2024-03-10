from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar

from backend.models import BaseModel

T = TypeVar('T', bound=BaseModel)


class IRepository(Generic[T], ABC):
    @abstractmethod
    def add(self, record: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, record_id: int) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, record: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, record_id: int) -> None:
        raise NotImplementedError


class IRepositoryInMemory(IRepository[T]):
    # Protected attributes
    _id: int = 1
    _data: Dict[int, T] = {}

    def add(self, record: T) -> T:
        # All items here has auto increment id
        record.id = self._id

        self._data[self._id] = record
        self._id += 1

        return record

    def get_by_id(self, record_id: int) -> Optional[T]:
        if record_id in self._data:
            return self._data[record_id]

        return None

    def get_all(self) -> List[T]:
        return list(self._data.values())

    def update(self, record: T) -> T:
        if record.id in self._data:
            self._data[record.id] = record

        return record

    def delete(self, record_id: int) -> None:
        if record_id in self._data:
            del self._data[record_id]
