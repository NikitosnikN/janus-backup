from typing import Optional

from cryptography.fernet import Fernet

from janusbackup.config import CONFIG_FACTORY, Config

__all__ = ["FernetWrapper"]


class FernetWrapper(Fernet):
    def __init__(self, config: Config = None):
        self.config = config or CONFIG_FACTORY()

        super().__init__(config.SECRET)

    def encrypt(self, data: str) -> str:
        return super().encrypt(data.encode("utf-8")).decode("utf-8")

    def decrypt(self, token: str, ttl: Optional[int] = None) -> str:
        return super().decrypt(token.encode("utf-8"), ttl).decode("utf-8")
