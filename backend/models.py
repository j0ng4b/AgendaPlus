from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BaseModel(ABC):
    id: int = field(init=False)


@dataclass
class User(BaseModel):
    name: str
    email: str
    password: str


@dataclass
class Task(BaseModel):
    summary: str
    description: str
    date: datetime
    user_id: int


@dataclass
class RefreshToken(BaseModel):
    iat: int
    user_id: int
