from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import create_db_and_tables
from app.api.main import api_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    create_db_and_tables()
    yield
    # Shutdown code here (if needed)


app = FastAPI(lifespan=lifespan)

# include routers here...
app.include_router(api_router)