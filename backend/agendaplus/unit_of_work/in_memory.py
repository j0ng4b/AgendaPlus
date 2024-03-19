from agendaplus.repository.refresh_token import RefreshTokenRepositoryInMemory
from agendaplus.repository.task import TaskRepositoryInMemory
from agendaplus.repository.user import UserRepositoryInMemory
from agendaplus.unit_of_work.generic import IUnitOfWork


class UnitOfWorkInMemory(IUnitOfWork):
    saved: bool = False

    def __init__(self) -> None:
        self.refresh_token = RefreshTokenRepositoryInMemory()
        self.task = TaskRepositoryInMemory()
        self.user = UserRepositoryInMemory()

    def save(self) -> None:
        self.saved = True

    def rollback(self) -> None:
        pass
