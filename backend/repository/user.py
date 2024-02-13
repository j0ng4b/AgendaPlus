from abc import ABC, abstractmethod
from typing import Optional

from . import IRepository, IRepositoryInMemory
from ..models import User

__all__ = [
    'IUserRepository',
    'UserRepositoryInMemory'
]


class IUserRepository(IRepository[User], ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError


class UserRepositoryInMemory(IUserRepository, IRepositoryInMemory[User]):
    def __init__(self) -> None:
        super().__init__()

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._data.values():
            if user.email == email:
                return user

        return None
