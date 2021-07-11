from fastapi import APIRouter, Depends

from .dependencies import BasePostRepository, get_post_repository
from .models import CreatePostParams, Post, DetailPost, UpdatePostParams


router = APIRouter()


@router.get("/", tags=["Posts"], response_model=list[Post])
async def list_posts(repository: BasePostRepository = Depends(get_post_repository)):
    posts = await repository.list_posts()
    return posts

@router.get("/{id}", tags=["Posts"], response_model=DetailPost)
async def particular_post(id: int, repository: BasePostRepository = Depends(get_post_repository)):
    post = await repository.detail_post(id)
    return post

@router.post("/", tags=["Posts"], response_model=Post, status_code=201)
async def create_post(
    post: CreatePostParams,
    repository: BasePostRepository = Depends(get_post_repository)
):
    post = await repository.create_post(post)
    return post

@router.put("/{id}", tags=["Posts"], status_code=200)
async def update_post(
    post: UpdatePostParams,
    id: int,
    repository: BasePostRepository = Depends(get_post_repository)
):
    post = await repository.update_post(post, id)
    return post
