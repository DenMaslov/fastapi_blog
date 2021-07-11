from pydantic import BaseModel
from ..users.models import User


class CreatePostParams(BaseModel):
    userId: int
    title: str
    body: str

class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User

class DetailPost(Post):
    comments: list

class UpdatePostParams(BaseModel):
    title: str
    body: str