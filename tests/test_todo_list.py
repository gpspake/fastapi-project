from database.todo_list import TodoList, TodoItem
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


def test_pydantic_todo_from_orm():
    assert PydanticTodoList.from_orm(orm_todo_list) == pydantic_todo_list


def test_pydantic_todo_list_to_dict():
    todo_list_dict = {
        'id': 1,
        'name': 'Groceries',
        'todo_items': [
            {'id': 1, 'name': 'Bread', 'is_complete': True, 'todo_list_id': 1},
            {'id': 2, 'name': 'Milk', 'is_complete': False, 'todo_list_id': 1}]
    }
    assert pydantic_todo_list.dict() == todo_list_dict


def test_pydantic_todo_list_to_dict_by_alias():
    todo_list_dict_by_alias = {
        'id': 1,
        'name': 'Groceries',
        'todoItems': [
            {'id': 1, 'name': 'Bread', 'isComplete': True, 'todoListId': 1},
            {'id': 2, 'name': 'Milk', 'isComplete': False, 'todoListId': 1}]
    }
    assert pydantic_todo_list.dict(by_alias=True) == todo_list_dict_by_alias
