from fastapi import APIRouter

from janusbackup.api.controllers import projects

# from janusbackup.config import SETTINGS

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
