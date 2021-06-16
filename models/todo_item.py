from pydantic import BaseModel, Field


class PydanticTodoItem(BaseModel):
    id: int
    name: str
    is_complete: bool = Field(alias='isComplete')
    todo_list_id: int = Field(alias='todoListId')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
