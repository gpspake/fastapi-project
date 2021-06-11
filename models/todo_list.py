from models.base_config import BaseConfig
from models.todo_item import TodoItem
from typing import List


class TodoList(BaseConfig):
    id: int
    name: str
    todo_items: List[TodoItem]
