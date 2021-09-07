from fastapi import APIRouter, Query

from janusbackup.database.models import LogModel

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def logs_fetch_all(
    page: int = Query(default=1, gt=0, description="Page number"),
    page_size: int = Query(default=10, ge=10, le=50, description="Page size"),
):
    return await LogModel.filter_paginated(page=page, page_size=page_size)
