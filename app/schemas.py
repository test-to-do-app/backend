from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.types import TaskOrderBy


class GetTasks(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page: int = 1
    order_by: Optional[TaskOrderBy | str] = Field(default=None, alias='orderBy')


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    username: str
    email: str
    description: str
    edited_by_administrator: bool = Field(alias='editedByAdministrator')
    is_completed: bool = Field(alias='isCompleted')


class Tasks(BaseModel):
    count: int
    items: list[Task]


class CreateTask(BaseModel):
    username: str = Field(max_length=256)
    email: str = Field(max_length=128)
    description: str


class EditTask(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    description: str
    is_completed: bool = Field(alias='isCompleted')


class LogIn(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str


class Ok(BaseModel):
    success: bool = True


class Error(BaseModel):
    success: bool = False
    detail: str
