from sqlalchemy.orm import relationship
from database.base import Base
from db_session import Session
from fastapi_auth0 import Auth0User
from sqlalchemy import Column, String
import uuid


class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    auth0_id = Column(String)
    email = Column(String)

    todo_lists = relationship(
        "TodoList", back_populates="user", cascade="all, delete, delete-orphan"
    )


def create_new_user(auth0_user: Auth0User) -> User:
    user = User(
        id=str(uuid.uuid4()),
        auth0_id=auth0_user.id,
        email=auth0_user.email)

    session = Session()
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user


def get_user(auth0_user: Auth0User) -> User:
    session = Session()
    user: User = session.query(User).filter_by(auth0_id=auth0_user.id).first()
    session.close()
    return create_new_user(auth0_user) if user is None else user
