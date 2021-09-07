from fastapi import status
from fastapi.exceptions import HTTPException
from starlette.requests import Request

__all__ = [
    "get_user",
    "auth_required",
    "superuser_required",
    "staff_or_superuser_required",
]


def get_user(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Auth is required")

    elif request.user and not request.user.is_active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "UserSchema is not active")

    return request.user


def auth_required(request: Request):
    return get_user(request)


def staff_or_superuser_required(request: Request):
    user = get_user(request)

    if not user.is_staff and not user.is_superuser:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "UserSchema has not enough permissions")
    else:
        return user


def superuser_required(request: Request):
    user = get_user(request)

    if not user.is_superuser:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "UserSchema has not enough permissions")
    else:
        return user
