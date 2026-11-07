from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  registers the tables
from app.database import create_tables
from app.routers import auth, games


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    create_tables()
    yield


app = FastAPI(title="GameJam API", version="1.0.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(games.router)
