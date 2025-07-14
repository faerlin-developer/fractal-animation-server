from pydantic import BaseModel


class UserIn(BaseModel):
    body: str


class User(UserIn):
    id: int
