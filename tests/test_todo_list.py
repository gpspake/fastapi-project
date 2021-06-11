from models.todo_item import TodoItem
from models.todo_list import TodoList

todo_list = TodoList(
        id=1,
        name='Groceries',
        todo_items=[
            TodoItem(id=1, name='Bread', is_complete=True, todo_list_id=1),
            TodoItem(id=2, name='Milk', is_complete=False, todo_list_id=1)
        ]
    )


def test_todo_list_dict():
    todo_list_dict = {
        'id': 1,
        'name': 'Groceries',
        'todo_items': [
            {'id': 1, 'name': 'Bread', 'is_complete': True, 'todo_list_id': 1},
            {'id': 2, 'name': 'Milk', 'is_complete': False, 'todo_list_id': 1}]
    }
    assert todo_list.dict() == todo_list_dict


def test_todo_list_dict_by_alias():
    todo_list_dict_by_alias = {
        'id': 1,
        'name': 'Groceries',
        'todoItems': [
            {'id': 1, 'name': 'Bread', 'isComplete': True, 'todoListId': 1},
            {'id': 2, 'name': 'Milk', 'isComplete': False, 'todoListId': 1}]
    }
    assert todo_list.dict(by_alias=True) == todo_list_dict_by_alias
