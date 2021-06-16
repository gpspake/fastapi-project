from pydantic import Field, BaseModel
from models.todo_item import PydanticTodoItem
from typing import List


class PydanticTodoList(BaseModel):
    id: int
    name: str
    todo_items: List[PydanticTodoItem] = Field(alias='todoItems')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
