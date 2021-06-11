from pydantic import BaseModel


def to_camel(string: str) -> str:
    first, *rest = string.split('_')
    return ''.join([first.lower(), *map(str.title, rest)])


class BaseConfig(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
