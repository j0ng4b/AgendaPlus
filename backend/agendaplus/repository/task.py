from abc import abstractmethod
from datetime import datetime
from typing import List

from agendaplus.models import Task
from agendaplus.repository.generic import IRepository, IRepositoryInMemory


class ITaskRepository(IRepository[Task]):
    @abstractmethod
    def get_by_date(self, user_id: int, date: datetime) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Task]:
        raise NotImplementedError


class TaskRepositoryInMemory(ITaskRepository, IRepositoryInMemory[Task]):
    def __init__(self) -> None:
        super().__init__()
        self._data = {}

    def get_by_date(self, user_id: int, date: datetime) -> List[Task]:
        tasks = []

        for task in self._data.values():
            if task.date is None:
                continue

            if task.user_id == user_id and task.date.date() == date.date:
                tasks.append(task)

        return tasks

    def get_by_user_id(self, user_id: int) -> List[Task]:
        tasks = []

        for task in self._data.values():
            if task.user_id == user_id:
                tasks.append(task)

        return tasks
