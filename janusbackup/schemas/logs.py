from enum import Enum

from .base import BaseModel, Field

__all__ = ["LogType", "LogDBPayload"]


class LogType(str, Enum):
    BACKUP_CRON_STARTED = "BACKUP_CRON_STARTED"
    BACKUP_CRON_FINISHED = "BACKUP_CRON_FINISHED"

    BACKUP_COMPLETED = "BACKUP_COMPLETED"

    FILE_UPLOADED = "FILE_UPLOADED"
    FILE_DELETED = "FILE_DELETED"

    LOGS_DELETED = "LOGS_DELETED"


class LogDBPayload(BaseModel):
    type: LogType = Field(...)
    payload: dict = Field(default={})
