from typing import List

from database.base import Base
from models.todo_list import PydanticTodoList
from sqlalchemy.orm import relationship
from database.user import User
from db_session import Session
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey


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


def get_todo_lists(user: User) -> List[PydanticTodoList]:
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
