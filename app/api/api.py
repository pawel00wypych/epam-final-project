from fastapi import APIRouter
from .endpoints import users, projects, documents # relative import

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(projects.router)
api_router.include_router(documents.router)