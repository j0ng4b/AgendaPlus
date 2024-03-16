from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Self, Type

from backend.repository.refresh_token import IRefreshTokenRepository
from backend.repository.task import ITaskRepository
from backend.repository.user import IUserRepository


class IUnitOfWork(ABC):
    refresh_token: IRefreshTokenRepository
    task: ITaskRepository
    user: IUserRepository

    def __enter__(self) -> Self:
        return self

    def __exit__(self,
                 exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 exception_traceback: Optional[TracebackType]) -> None:
        if exception_type is None:
            self.save()
        else:
            self.rollback()

    @abstractmethod
    def save(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
