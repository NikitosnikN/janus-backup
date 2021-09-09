from typing import Any, Dict, Optional

from fastapi import HTTPException, status

__all__ = ["ExtendedHTTPException"]


class ExtendedHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: int = -1,
        message: str = None,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.message = message
        self.headers = headers
