from models.base_config import BaseConfig


class TodoItem(BaseConfig):
    id: int
    name: str
    is_complete: bool
    todo_list_id: int
