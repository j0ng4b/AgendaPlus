from abc import abstractmethod
from typing import Optional

from agendaplus.models import RefreshToken
from agendaplus.repository.generic import IRepository, IRepositoryInMemory


class IRefreshTokenRepository(IRepository[RefreshToken]):
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[RefreshToken]:
        raise NotImplementedError


class RefreshTokenRepositoryInMemory(IRefreshTokenRepository,
                                     IRepositoryInMemory[RefreshToken]):
    def __init__(self) -> None:
        super().__init__()
        self._data = {}

    def get_by_user_id(self, user_id: int) -> Optional[RefreshToken]:
        for token in self._data.values():
            if token.user_id == user_id:
                return token

        return None
