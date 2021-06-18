from typing import List
from database.base import Base
from models.todo_item import PydanticTodoItem
from models.todo_list import PydanticTodoList
from sqlalchemy.orm import relationship
from db_session import Session
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, update
from models.user import PydanticUser


class TodoList(Base):
    __tablename__ = 'todo_list'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column('user_id', Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="todo_lists")
    todo_items = relationship(
        "TodoItem", back_populates="todo_list", cascade="all, delete, delete-orphan"
    )


class TodoItem(Base):
    __tablename__ = 'todo_item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_complete = Column(Boolean)
    todo_list_id = Column(Integer, ForeignKey('todo_list.id'))
    todo_list = relationship("TodoList", back_populates="todo_items")


def get_todo_lists(user: PydanticUser) -> List[PydanticTodoList]:
    session = Session()
    results = session.query(TodoList).filter_by(user_id=user.id).all()
    todo_lists = [PydanticTodoList.from_orm(todo_list) for todo_list in results]
    session.close()
    return todo_lists


def get_todo_list(todo_list_id: int) -> PydanticTodoList:
    session = Session()
    result = session.query(TodoList).filter_by(todo_list_id=todo_list_id).first()
    todo_list = PydanticTodoList.from_orm(result)
    session.close()
    return todo_list


def put_todo_list(todo_list: PydanticTodoList) -> PydanticTodoList:
    session = Session()
    stmt = update(TodoList).where(TodoList.id == todo_list.id).values(name=todo_list.name). \
        execution_options(synchronize_session="fetch")
    updated_todo_list = session.execute(stmt)
    pydantic_todo_list = PydanticTodoList.from_orm(updated_todo_list)
    session.close()
    return pydantic_todo_list


def create_todo_list(new_todo_list: PydanticTodoList, user: PydanticUser) -> PydanticTodoList:
    todo_items = []
    for todo_item in new_todo_list.todo_items:
        todo_item_dict = todo_item.dict()
        todo_item_dict.pop('id')
        todo_item_dict.pop('todo_list_id')
        todo_items.append(TodoItem(**todo_item_dict))

    todo_list_dict = new_todo_list.dict()
    todo_list_dict.pop('id')
    todo_list_dict['todo_items'] = []
    todo_list = TodoList(**todo_list_dict)
    todo_list.user_id = user.id
    todo_list.todo_items = todo_items

    session = Session()
    session.add(todo_list)
    session.commit()
    session.refresh(todo_list)
    pydantic_todo_list = PydanticTodoList.from_orm(todo_list)
    session.close()
    return pydantic_todo_list


def create_todo_item(new_todo_item: PydanticTodoItem) -> PydanticTodoItem:
    todo_item_dict = new_todo_item.dict()
    todo_item_dict.pop('id')
    todo_item = TodoItem(**todo_item_dict)
    session = Session()
    session.add(todo_item)
    session.commit()
    session.refresh(todo_item)
    pydantic_todo_item = PydanticTodoItem.from_orm(todo_item)
    session.close()
    return pydantic_todo_item
