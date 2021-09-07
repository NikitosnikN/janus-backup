from abc import ABC, abstractmethod
from datetime import datetime
from os import path
from typing import Optional, Union

from janusbackup.database.models import ProjectModel
from janusbackup.schemas import BaseModel, ProjectSchema


class BaseBackupProvider(ABC):
    params_schema: Optional[BaseModel] = None
    _backup_path: str
    _generated_filename: Optional[str]
    project_title: str = ""

    @property
    @abstractmethod
    def db_type(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def start_backup(cls, **kwargs) -> "BaseBackupProvider":
        pass

    @abstractmethod
    async def _load_provider_params(self) -> dict:
        pass

    @classmethod
    def from_project(cls, project: ProjectModel, **kwargs):
        pass

    @classmethod
    def from_schema(cls, project: ProjectSchema, **kwargs):
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
