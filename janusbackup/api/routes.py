from fastapi import APIRouter

from janusbackup.api.controllers import debug, logs, projects
from janusbackup.config import DEBUG

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])

if DEBUG:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
