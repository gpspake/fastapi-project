import os
from typing import List

from models.user import PydanticUser
from models.todo_item import PydanticTodoItem
from models.todo_list import PydanticTodoList
from database.todo_list import get_todo_lists, create_todo_item, TodoItem
from database.user import get_user, User
from fastapi import FastAPI, Depends, Security, HTTPException, status
from fastapi_auth0 import Auth0, Auth0User

auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_api_audience = os.getenv('AUTH0_API_AUDIENCE')

auth = Auth0(domain=auth0_domain, api_audience=auth0_api_audience, scopes={'read:hello': 'Read Hello'})
app = FastAPI()


@app.get("/api/TodoLists", dependencies=[Depends(auth.implicit_scheme)])
def get_secure_todo_lists(auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    todo_lists: List[PydanticTodoList] = get_todo_lists(user=user)
    data = [todo_list.dict(by_alias=True) for todo_list in todo_lists]
    return {"data": data}


@app.post("/api/TodoItems", dependencies=[Depends(auth.implicit_scheme)])
def add_todo_item(new_todo_item: PydanticTodoItem, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    if user.has_todo_list(new_todo_item.todo_list_id):
        todo_item: PydanticTodoItem = create_todo_item(new_todo_item)
        return {"todo_item": todo_item.dict(by_alias=True)}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Todo list not found",
            headers={"WWW-Authenticate": "Basic"})


if __name__ == '__main__':
    import uvicorn
    reload = True
    uvicorn.run("main:app", host='0.0.0.0', port=8009, reload=reload)
