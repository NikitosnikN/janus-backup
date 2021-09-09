from typing import Optional, Tuple

from starlette.authentication import AuthCredentials, AuthenticationBackend

__all__ = [
    "JWTAuthBackend",
]


class JWTAuthBackend(AuthenticationBackend):
    @staticmethod
    async def _auth_with_jwt(header: str) -> Optional[dict]:
        if not header or not isinstance(header, str):
            return None

        if header:
            header = header.split(" ")

        if len(header) == 2 and header[0] == "Bearer":
            header[1]
            # find by token
            return

        return None

    async def authenticate(self, request) -> Optional[Tuple[AuthCredentials, dict]]:
        user = await self._auth_with_jwt(request.headers.get("authorization") or request.headers.get("Authorization"))

        if user:
            scopes = {
                "authenticated": True,
                "is_superuser": user.is_superuser,
            }
            return AuthCredentials([key for key, val in scopes.items() if val]), user

        return None
