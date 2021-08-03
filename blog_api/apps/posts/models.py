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

class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str 

class DetailPost(Post):
    comments: list[Comment]

class UpdatePostParams(BaseModel):
    title: str
    body: str