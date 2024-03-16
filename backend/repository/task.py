from abc import abstractmethod
from typing import Optional

from backend.models import Task
from backend.repository.generic import IRepository, IRepositoryInMemory


class ITaskRepository(IRepository[Task]):
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Task]:
        raise NotImplementedError


class TaskRepositoryInMemory(ITaskRepository, IRepositoryInMemory[Task]):
    def __init__(self) -> None:
        super().__init__()
        self._data = {}

    def get_by_user_id(self, user_id: int) -> Optional[Task]:
        for task in self._data.values():
            if task.user_id == user_id:
                return task

        return None