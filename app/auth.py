from db_session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import uuid
import random
import string

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    auth0_id = Column(String)
    email = Column(String)


def create_new_user(user: User):
    session = Session()
    session.add(user)
    session.commit()
    session.close()


create_new_user(User(
    id=str(uuid.uuid4()),
    auth0_id=str(uuid.uuid4()),
    email=''.join(random.choice(string.ascii_letters) for _ in range(7)) + "@gmail.com"
))