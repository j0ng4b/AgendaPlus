from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from kink import inject

from agendaplus.models import Task
from agendaplus.unit_of_work.generic import IUnitOfWork


class ITaskService(ABC):
    _uow: IUnitOfWork

    @abstractmethod
    def add(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get_by_date(self, user_id: int, date: datetime) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_by_id(self, user_id: int, task_id: int) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> None:
        raise NotImplementedError


@inject
class TaskService(ITaskService):
    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    def add(self, task: Task) -> Task:
        new_task = self._uow.task.add(task)
        self._uow.save()

        return new_task

    def get_by_date(self, user_id: int, date: datetime) -> List[Task]:
        return self._uow.task.get_by_date(user_id, date)

    def get_by_user_id(self, user_id: int) -> List[Task]:
        return self._uow.task.get_by_user_id(user_id)

    def get_by_user_by_id(self, user_id: int, task_id: int) -> Optional[Task]:
        tasks = self._uow.task.get_by_user_id(user_id)
        for task in tasks:
            if task.id == task_id:
                return task

        return None

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._uow.task.get_by_id(task_id)

    def get_all(self) -> List[Task]:
        return self._uow.task.get_all()

    def update(self, task: Task) -> Task:
        updated_task = self._uow.task.update(task)
        self._uow.save()

        return updated_task

    def delete(self, task_id: int) -> None:
        if self._uow.task.get_by_id(task_id) is None:
            return

        self._uow.task.delete(task_id)
        self._uow.save()
