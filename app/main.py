import os
from typing import List
from models.user import PydanticUser
from models.todo_item import PydanticTodoItem
from models.todo_list import PydanticTodoList
from database.todo_list import orm_delete_todo_item, orm_delete_todo_list, orm_read_todo_list, orm_create_todo_list, \
    orm_update_todo_list, orm_create_todo_item, orm_update_todo_item, orm_read_todo_item, orm_read_todo_lists
from database.user import get_user
from fastapi import FastAPI, Depends, Security, HTTPException, status
from fastapi_auth0 import Auth0, Auth0User

auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_api_audience = os.getenv('AUTH0_API_AUDIENCE')

auth = Auth0(domain=auth0_domain, api_audience=auth0_api_audience, scopes={'read:hello': 'Read Hello'})
app = FastAPI()


@app.get("/api/TodoLists", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo Lists"])
def read_todo_lists(auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    todo_lists: List[PydanticTodoList] = orm_read_todo_lists(user=user)
    data = [todo_list.dict(by_alias=True) for todo_list in todo_lists]
    return data


@app.post("/api/TodoLists", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo List"])
def create_todo_list(new_todo_list: PydanticTodoList, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    todo_list: PydanticTodoList = orm_create_todo_list(new_todo_list, user)
    return todo_list.dict(by_alias=True)


@app.get("/api/TodoLists/{todo_list_id}", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo List"])
def read_todo_list(todo_list_id: int, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    if user.has_todo_list(todo_list_id):
        todo_list: PydanticTodoList = orm_read_todo_list(todo_list_id)
        return todo_list
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Todo list not found",
            headers={"WWW-Authenticate": "Basic"})


@app.put("/api/TodoLists/{TodoListId}", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo List"])
def update_todo_list(todo_list: PydanticTodoList, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    if user.has_todo_list(todo_list.id):
        updated_todo_list: PydanticTodoList = orm_update_todo_list(todo_list.id, todo_list.name)
        return updated_todo_list.dict(by_alias=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Todo list not found",
            headers={"WWW-Authenticate": "Basic"})


@app.delete("/api/TodoLists/{todo_list_id}", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo List"])
def delete_todo_list(todo_list_id: int, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    todo_list = orm_read_todo_list(todo_list_id=todo_list_id)
    if user.has_todo_list(todo_list.id):
        return orm_delete_todo_list(todo_list.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Todo list not found",
            headers={"WWW-Authenticate": "Basic"})


@app.post("/api/TodoItems", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo Item"])
def create_todo_item(new_todo_item: PydanticTodoItem, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    if user.has_todo_list(new_todo_item.todo_list_id):
        todo_item: PydanticTodoItem = orm_create_todo_item(new_todo_item)
        return todo_item.dict(by_alias=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Todo list not found",
            headers={"WWW-Authenticate": "Basic"})


@app.put("/api/TodoItems/{todo_item_id}", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo Item"])
def update_todo_item(todo_item: PydanticTodoItem, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    if user.has_todo_list(todo_item.todo_list_id):
        updated_todo_item: PydanticTodoItem = orm_update_todo_item(todo_item.id, todo_item.name, todo_item.is_complete)
        return updated_todo_item.dict(by_alias=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Todo list not found",
            headers={"WWW-Authenticate": "Basic"})


@app.delete("/api/TodoItems/{todo_item_id}", dependencies=[Depends(auth.implicit_scheme)], tags=["Todo Item"])
def delete_todo_item(todo_item_id: int, auth0_user: Auth0User = Security(auth.get_user)):
    user: PydanticUser = get_user(auth0_user=auth0_user)
    todo_item = orm_read_todo_item(todo_item_id=todo_item_id)
    if user.has_todo_list(todo_item.todo_list_id):
        return orm_delete_todo_item(todo_item_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Todo list not found",
            headers={"WWW-Authenticate": "Basic"})


if __name__ == '__main__':
    import uvicorn
    reload = True
    uvicorn.run("main:app", host='0.0.0.0', port=8009, reload=reload)
