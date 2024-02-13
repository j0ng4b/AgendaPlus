from dataclasses import dataclass
from typing import Protocol


@dataclass
class BaseModel(Protocol):
    id: int


@dataclass
class User(BaseModel):
    name: str
    email: str
    password: str
