from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:////tmp/todo.db", future=True, echo=True)
Session = sessionmaker(bind=engine)
