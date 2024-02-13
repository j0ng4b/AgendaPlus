from abc import ABC, abstractmethod
from typing import List, Optional

from kink import inject

from ..models import User
from ..unit_of_work import IUnitOfWork


class IUserService(ABC):
    _uow: IUnitOfWork

    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> None:
        raise NotImplementedError


@inject
class UserService(IUserService):
    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    def add(self, user: User) -> User:
        new_user = self._uow.user.add(user)
        self._uow.save()

        return new_user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._uow.user.get_by_id(user_id)

    def get_all(self) -> List[User]:
        return self._uow.user.get_all()

    def get_by_email(self, email: str) -> Optional[User]:
        return self._uow.user.get_by_email(email)

    def update(self, user: User) -> User:
        updated_user = self._uow.user.update(user)
        self._uow.save()

        return updated_user

    def delete(self, user_id: int) -> None:
        if self._uow.user.get_by_id(user_id) is None:
            return

        self._uow.user.delete(user_id)
        self._uow.save()
