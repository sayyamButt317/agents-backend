from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.connection import close, connect


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect()
    yield
    close()


app = FastAPI(lifespan=lifespan)
