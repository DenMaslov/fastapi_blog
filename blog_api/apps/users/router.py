from fastapi import APIRouter, Depends

from .dependencies import BaseUserRepository, get_user_repository
from .models import CreateUserParams, User


router = APIRouter()


@router.get("/", tags=["users"], response_model=list[User])
async def list_users(repository: BaseUserRepository = Depends(get_user_repository)):
    users = await repository.list_users()
    return users


@router.post("/", tags=["users"], response_model=User, status_code=201)
async def create_user(
    user: CreateUserParams,
    repository: BaseUserRepository = Depends(get_user_repository)
):
    user = await repository.create_user(user)
    return user

