from fastapi import FastAPI

from app.database import engine
from app.models import models
from app.routers import auth, companies, tasks, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App API", version="1.0.0")

app.include_router(auth.router, tags=["authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(companies.router, prefix="/api/v1", tags=["companies"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Todo App API"}
