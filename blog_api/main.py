from fastapi import FastAPI
import logging as log

from apps.posts import router as post_router
from apps.users import router as user_router


rootLog = log.getLogger()
rootLog.setLevel(log.INFO)
log.basicConfig(format='%(message)s')


def create_app():
    app = FastAPI()
    app.include_router(post_router, prefix="/posts")
    app.include_router(user_router, prefix="/users")
    return app


app = create_app()
