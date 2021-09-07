from fastapi import APIRouter, Body, HTTPException, Path, Query, Response, status

from janusbackup.core.exceptions import ExtendedHTTPException
from janusbackup.core.mechanics import BackupPipeline
from janusbackup.database.models import ProjectModel
from janusbackup.schemas import ProjectCreateSchema, ProjectSchema, ProjectSchemaPaginated, ProjectUpdateSchema

__all__ = ["router"]

router = APIRouter()


@router.get("/", response_model=ProjectSchemaPaginated)
async def projects_fetch_all(
    page: int = Query(default=1, gt=0, description="Page number"),
    page_size: int = Query(default=10, ge=10, le=50, description="Page size"),
):
    return await ProjectModel.filter_paginated(page=page, page_size=page_size)


@router.get("/{project_id}/", response_model=ProjectSchema)
async def projects_fetch_one(
    project_id: int = Path(...),
):
    project = await ProjectModel.get_or_none(id=project_id)

    if not project:
        raise ExtendedHTTPException(status_code=404, detail="object not found")

    return project


@router.post("/", response_model=ProjectSchema)
async def projects_create(payload: ProjectCreateSchema = Body(...)):
    if await ProjectModel.filter(title=payload.title).exists():
        raise ExtendedHTTPException(message=f"project with {payload.title} already exists")

    project = ProjectModel(**payload.dict(exclude={"id"}))
    await project.save()
    return project


@router.put("/{project_id}/", response_model=ProjectSchema)
async def projects_update(project_id: int = Path(...), payload: ProjectUpdateSchema = Body(...)):
    project = await ProjectModel.get_or_none(id=project_id)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(project, k, v)

    await project.save()
    return project


@router.post("/{project_id}/run-backup/")
async def projects_run_backup(
    project_id: int = Path(...),
):
    project = await ProjectModel.get_or_none(id=project_id)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")

    await BackupPipeline.run_pipeline_for_project(project)

    return True


@router.delete("/{project_id}/")
async def projects_delete(
    project_id: str = Path(...),
):
    project = await ProjectModel.get_or_none(id=project_id)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")

    await project.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
