from fastapi import responses
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request

from janusbackup.api.exceptions import ExtendedHTTPException

__all__ = ["exception_handlers"]


async def pydantic_exception_handler_func(request: Request, exception: ValidationError):
    errors = []
    for error in exception.errors():
        errors.append(
            {
                "field": error["loc"][-1],
                "message": error.get("msg"),
                "type": error.get("type"),
            }
        )
    return responses.UJSONResponse(
        content={"error_code": 422, "message": "validation error", "details": errors},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        headers={"Access-Control-Allow-Origin": "*"},
    )


async def http_exc_handler(request: Request, exception: HTTPException):
    return responses.UJSONResponse(
        content={"error_code": -1, "message": exception.detail, "details": {}},
        status_code=getattr(exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        headers={"Access-Control-Allow-Origin": "*"},
    )


async def extended_http_exc_handler(request: Request, exception: ExtendedHTTPException):
    return responses.UJSONResponse(
        content={
            "error_code": exception.error_code,
            "message": exception.message,
            "details": exception.detail or {},
        },
        status_code=getattr(exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        headers={"Access-Control-Allow-Origin": "*"},
    )


exception_handlers = {
    ExtendedHTTPException: extended_http_exc_handler,
    HTTPException: http_exc_handler,
    RequestValidationError: pydantic_exception_handler_func,
    ValidationError: pydantic_exception_handler_func,
}
