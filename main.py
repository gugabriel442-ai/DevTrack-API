
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import Base, engine

# Importação dos modelos
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

# Importação das rotas
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.api.routes.projects import router as projects_router
from app.api.routes.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="DevTrack API",
    description="API para gerenciamento de projetos e tarefas",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

# Registro das rotas
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "DevTrack API está funcionando!"
    }


@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected"
    }
app.include_router(projects_router)
app.include_router(tasks_router)