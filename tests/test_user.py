from models.user import PydanticUser
from fixtures import pydantic_user, orm_user


def test_pydantic_todo_from_orm():
    assert PydanticUser.from_orm(orm_user) == pydantic_user


def test_user_has_todo_list():
    assert PydanticUser.has_todo_list(pydantic_user, todo_list_id=1)
    assert PydanticUser.has_todo_list(pydantic_user, todo_list_id=2) is False
