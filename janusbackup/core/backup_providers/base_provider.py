import os
from abc import ABC, abstractmethod
from datetime import datetime
from os import path
from typing import Optional, Union

from janusbackup.config import CONFIG_FACTORY, Config
from janusbackup.schemas import BaseModel, DBType, ProjectSchema


class BaseBackupProvider(ABC):
    db_type: DBType
    params_schema: Optional[BaseModel] = None

    def __init__(self, project: ProjectSchema, config: Config = None, **kwargs):
        self.project = project
        self.config = config or CONFIG_FACTORY

        self._backup_path = "./.tmp/"
        self._generated_filename = None

    @property
    @abstractmethod
    def db_type(self) -> str:
        pass

    @classmethod
    @abstractmethod
    async def start_backup(cls, **kwargs) -> "BaseBackupProvider":
        pass

    @abstractmethod
    async def _load_provider_params(self) -> dict:
        pass

    @property
    def filename(self):
        return self._generated_filename

    @property
    def backup_filepath(self) -> str:
        if not self._generated_filename:
            raise ValueError("Backup filename is empty!")

        return path.join(self._backup_path, self._generated_filename)

    def _generate_filename(self, task_id: Union[str, int], backup_extension: str) -> str:
        self._generated_filename = (
            f"{self.db_type}_{task_id}_{datetime.utcnow().replace(microsecond=0).isoformat()}.{backup_extension}"
        )

        return self._generated_filename

    def validate_backup_exists(self) -> bool:
        return path.exists(self.backup_filepath)

    def remove_backup(self) -> None:
        os.remove(self.backup_filepath)
        return None
