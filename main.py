from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api import api_router
from app.db.connection import close, connect
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect()
    yield
    close()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
