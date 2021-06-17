from database.user import User

from database.todo_list import TodoList, TodoItem
from models.user import PydanticUser
from models.todo_item import PydanticTodoItem
from models.todo_list import PydanticTodoList


pydantic_todo_item_1 = PydanticTodoItem(id=1, name='Bread', is_complete=True, todo_list_id=1)
pydantic_todo_item_2 = PydanticTodoItem(id=2, name='Milk', is_complete=False, todo_list_id=1)

orm_todo_item_1 = TodoItem(id=1, name='Bread', is_complete=True, todo_list_id=1)
orm_todo_item_2 = TodoItem(id=2, name='Milk', is_complete=False, todo_list_id=1)

pydantic_todo_list = PydanticTodoList(
    id=1,
    name='Groceries',
    todo_items=[pydantic_todo_item_1, pydantic_todo_item_2])

orm_todo_list = TodoList(
    id=1,
    name='Groceries',
    todo_items=[orm_todo_item_1, orm_todo_item_2],
    user_id='555',
)

pydantic_user = PydanticUser(
    id=1,
    auth0_id='55555',
    email='foo@bar.com',
    todo_lists=[pydantic_todo_list]
)

orm_user = User(
    id=1,
    auth0_id='55555',
    email='foo@bar.com',
    todo_lists=[orm_todo_list]
)
