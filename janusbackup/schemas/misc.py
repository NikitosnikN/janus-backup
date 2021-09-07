from .base import BaseModel, Field

__all__ = ["SuccessResponse", "NotFoundResponse"]


class BaseResponse(BaseModel):
    success: bool = Field(default=True)
    error_code: str = Field(default=None)
    error_detail: str = Field(default=None)


class SuccessResponse(BaseResponse):
    success: bool = True


class NotFoundResponse(BaseResponse):
    success: bool = False
    error_code: str = "404"
    error_detail: str = "Object not found"
