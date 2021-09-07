from datetime import datetime
from typing import List, Optional

from janusbackup.database.models import ConnectionType, DBType

from .base import BaseModelORM, BasePaginator, Field

__all__ = [
    "ProjectSchema",
    "ProjectUpdateSchema",
    "ProjectCreateSchema",
    "ProjectSchemaPaginated",
    "ConnectionType",
    "DBType",
]


class BaseProject(BaseModelORM):
    connection_type: ConnectionType = Field(...)

    # HOST

    host: Optional[str] = Field(default=None)
    host_user: Optional[str] = Field(default=None)
    host_password: Optional[str] = Field(default=None)

    # DB
    connection_schema: str = Field(...)
    connection_params: dict = Field(default={})

    db_type: DBType = Field(...)

    db_host: Optional[str] = Field(default=None)
    db_port: Optional[int] = Field(default=None, gt=0)

    db_name: Optional[str] = Field(...)
    db_username: Optional[str] = Field(...)
    db_password: Optional[str] = Field(...)

    is_dockerized: bool = Field(default=True)
    provider_params: dict = Field(default={})


class ProjectCreateSchema(BaseProject):
    title: str = Field(...)


class ProjectUpdateSchema(BaseProject):
    db_type: DBType = Field(default=None)
    db_name: Optional[str] = Field(default=None)
    db_username: Optional[str] = Field(default=None)
    db_password: Optional[str] = Field(default=None)
    connection_schema: str = Field(default=None)


class ProjectSchema(BaseProject):
    id: int = Field(default=None)
    title: str = Field(...)
    updated_at: Optional[datetime] = Field(default=None)
    last_backup_at: Optional[datetime] = Field(default=None)


class ProjectSchemaPaginated(BasePaginator):
    result: List[ProjectSchema] = Field(default=[])
