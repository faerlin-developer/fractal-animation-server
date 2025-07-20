from pydantic import BaseModel


class UserRequestPayload(BaseModel):
    username: str
    password: str


class SignUpResponsePayload(BaseModel):
    id: int
    username: str


class SignInResponsePayload(BaseModel):
    access_token: str
    token_type: str
