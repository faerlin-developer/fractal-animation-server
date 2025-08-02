from pydantic import BaseModel


class UserRequest(BaseModel):
	username: str
	password: str


class SignUp(UserRequest):
	id: int


class SignIn(BaseModel):
	access_token: str
	token_type: str
