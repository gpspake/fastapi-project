from typing import List
from pydantic import BaseModel
from models.todo_list import PydanticTodoList


class PydanticUser(BaseModel):
    id: str
    auth0_id: str
    email: str
    todo_lists: List[PydanticTodoList]

    class Config:
        orm_mode = True

    def has_todo_list(self, todo_list_id: int):
        return any(todo_lists.id == todo_list_id for todo_lists in self.todo_lists)
