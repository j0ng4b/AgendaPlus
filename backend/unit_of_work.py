from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Self, Type

from backend.repository.user import IUserRepository, UserRepositoryInMemory


class IUnitOfWork(ABC):
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


class UnitOfWorkInMemory(IUnitOfWork):
    saved: bool = False

    def __init__(self) -> None:
        self.user = UserRepositoryInMemory()

    def save(self) -> None:
        self.saved = True

    def rollback(self) -> None:
        pass
