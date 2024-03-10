from abc import abstractmethod
from typing import Optional

from backend.models import User
from backend.repository.generic import IRepository, IRepositoryInMemory


class IUserRepository(IRepository[User]):
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
