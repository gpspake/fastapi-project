import os
from typing import Optional, List
from models.todo_list import PydanticTodoList
from database.todo_list import get_todo_lists
from database.user import get_user, User
from fastapi import FastAPI, Depends, Security
from fastapi_auth0 import Auth0, Auth0User
import sqlalchemy

auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_api_audience = os.getenv('AUTH0_API_AUDIENCE')

auth = Auth0(domain=auth0_domain, api_audience=auth0_api_audience, scopes={'read:hello': 'Read Hello'})
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": sqlalchemy.__version__}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/secure/hello", dependencies=[Depends(auth.implicit_scheme)])
def get_secure_hello(user: Auth0User = Security(auth.get_user)):
    return {"hello": f"{user}"}


@app.get("/secure/hello2")
def get_secure_hello2(user: Auth0User = Security(auth.get_user, scopes=["read:hello"])):
    return {"hello": f"{user}"}


@app.get("/api/TodoLists", dependencies=[Depends(auth.implicit_scheme)])
def get_secure_todo_lists(auth0_user: Auth0User = Security(auth.get_user)):
    user: User = get_user(auth0_user=auth0_user)
    todo_lists: List[PydanticTodoList] = get_todo_lists(user=user)
    data = [todo_list.dict(by_alias=True) for todo_list in todo_lists]
    return {"data": data}


if __name__ == '__main__':
    import uvicorn
    reload = True
    uvicorn.run("main:app", host='0.0.0.0', port=8009, reload=reload)
