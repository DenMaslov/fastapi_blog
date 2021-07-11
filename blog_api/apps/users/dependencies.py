import weakref
import asyncio
import logging as log
from typing import Any
from aiohttp import ClientSession
from abc import ABC, abstractmethod

from .models import CreateUserParams, User




class BaseUserRepository(ABC):
    """ UserRepository interface """

    @abstractmethod
    async def create_user(self, user: CreateUserParams) -> User:
        pass

    @abstractmethod
    async def list_users(self) -> list[User]:
        pass


class JSONPlaceholderUserRepository(BaseUserRepository):

    def __init__(self):
        self._endpoint = "https://jsonplaceholder.typicode.com/users"
        self._finalizer = weakref.finalize(self, self.close_session)
        self._session = None
    
    async def start_session(self) -> None:
        if not self._session:
            log.info(f"Create session in obj {id(self)}")
            self._session = ClientSession()

    def close_session(self) -> None:
        if self._session:
            log.info(f"Close session in obj {id(self)}")
            asyncio.run(self._session.close())

    async def create_user(self, user: CreateUserParams) -> User:
        raw_user = await self._create_user(user)
        return self._convert_user(raw_user)

    async def list_users(self) -> list[User]:
        raw_users = await self._list_users()
        return [self._convert_user(raw_user) for raw_user in raw_users]

    async def _create_user(self, user: CreateUserParams) -> dict[str, Any]:
        resp = await self._session.post(self._endpoint, json=user.dict())
        raw_user = await resp.json()
        return raw_user

    async def _list_users(self) -> list[dict[str, Any]]:
        resp = await self._session.get(self._endpoint)
        raw_users = await resp.json()
        return raw_users

    def _convert_user(self, raw_user: dict[str, Any]) -> User:
        return User(**raw_user)


class UserRepositoryFactory:

    def __init__(self):
        self._repo = None

    async def __call__(self) -> BaseUserRepository:
        if self._repo is None:
            self._repo = JSONPlaceholderUserRepository()
            await self._repo.start_session()
        return self._repo


get_user_repository = UserRepositoryFactory()
