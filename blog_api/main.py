from fastapi import FastAPI
import logging as log

from .apps import posts, users


rootLog = log.getLogger()
rootLog.setLevel(log.INFO)
log.basicConfig(format='%(message)s')


def create_app():
    app = FastAPI()
    app.include_router(posts.router, prefix="/posts")
    app.include_router(users.router, prefix="/users")
    return app


app = create_app()
