from pydantic import BaseModel


class ImageIn(BaseModel):
    body: str


class Image(ImageIn):
    id: int
