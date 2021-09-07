from fastapi import APIRouter

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def debug_get():
    return {}


@router.post("/")
async def debug_post():
    return {}
