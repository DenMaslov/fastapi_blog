import asyncio
import weakref
import logging as log
from typing import Any
from aiohttp import ClientSession
from abc import ABC, abstractmethod

from ..users.models import User
from .models import CreatePostParams, Post, DetailPost, UpdatePostParams


class BasePostRepository(ABC):
    """ PostRepository interface """

    @abstractmethod
    async def create_post(self, post: CreatePostParams) -> Post:
        pass

    @abstractmethod
    async def list_posts(self) -> list[Post]:
        pass

    @abstractmethod
    async def detail_post(self, id: int) -> DetailPost:
        pass

    @abstractmethod
    async def update_post(self, post: UpdatePostParams, id: int) -> dict[str, Any]:
        pass


class PostRepository(BasePostRepository):

    def __init__(self) -> None:
        self._endpoint = "https://jsonplaceholder.typicode.com/posts"
        self._endpoint_author = "https://jsonplaceholder.typicode.com/users/"
        self._endpoint_comment = "https://jsonplaceholder.typicode.com/comments?postId="
        self._session = None
        self._authors: list[User] = []
        self._finalizer = weakref.finalize(self, self.close_session)
    
    async def start_session(self) -> None:
        if not self._session:
            log.info(f"Create session in obj {id(self)}")
            self._session = ClientSession()

    def close_session(self) -> None:
        if self._session:
            log.info(f"Close session in obj {id(self)}")
            asyncio.run(self._session.close())

    async def create_post(self, post: CreatePostParams) -> Post:
        raw_post = await self._create_post(post)
        return self._convert_post(raw_post)

    async def list_posts(self) -> list[Post]:
        raw_posts = await self._list_posts()
        return [self._convert_post(raw_post) for raw_post in raw_posts]
    
    async def detail_post(self, id: int) -> DetailPost:
        raw_post = await self._detail_post(id)
        return DetailPost(**raw_post)
    
    async def update_post(self, post: UpdatePostParams, id: int) -> dict[str, Any]:
            resp = await self._update_post(post, id)
            return resp
 
    async def _create_post(self, post: CreatePostParams) -> dict[str, Any]:
            resp = await self._session.post(self._endpoint, json=post.dict())
            raw_post = await resp.json()
            await self._list_authors()
            raw_post["author"] = await self._get_author_by_id(raw_post["userId"])
            return raw_post

    async def _list_posts(self) -> list[dict[str, Any]]:
            resp = await self._session.get(self._endpoint)
            raw_posts = await resp.json()
            await self._list_authors()
            await self._match_authors_and_posts(raw_posts)
            return raw_posts
    
    async def _detail_post(self, id: int) -> dict[str, Any]:
            resp = await self._session.get(self._endpoint + f"/{id}")
            detail_post = await resp.json()
            detail_post["comments"] = await self._get_comments(id)
            detail_post["author"] = await self._get_author(detail_post["userId"])
            return detail_post

    async def _update_post(self, post: UpdatePostParams, id: int) -> dict[str, Any]:
            resp = await self._session.put(self._endpoint + f"/{id}" ,
                                           json=post.dict())
            resp = await resp.json()
            return resp

    async def _list_authors(self) -> None:
            resp = await self._session.get(self._endpoint_author)
            self._authors = await resp.json()
    
    async def _get_author(self, id: int) -> dict[str, Any]:
            resp = await self._session.get(self._endpoint_author + f"/{id}")
            return await resp.json()
    
    async def _match_authors_and_posts(self, raw_posts: dict[str, Any]):
        for post in raw_posts:
            author = await self._get_author_by_id(post["userId"])
            post["author"] = author

    async def _get_author_by_id(self, id: int) -> dict[str, Any]:
        for author in self._authors:
            if author["id"] == id:
                return author
        return None
    
    async def _get_comments(self, postId: int) -> dict[str, Any]:
            resp = await self._session.get(self._endpoint_comment + str(postId))
            comments = await resp.json()
            return comments

    def _convert_post(self, raw_post: dict[str, Any]) -> Post:    
        return Post(**raw_post)


class PostRepositoryFactory:

    def __init__(self):
        self._repo = None

    async def __call__(self) -> BasePostRepository:
        if self._repo is None:
            self._repo = PostRepository()
            await self._repo.start_session()
        return self._repo


get_post_repository = PostRepositoryFactory()
