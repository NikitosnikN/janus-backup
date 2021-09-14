from sqlalchemy import JSON, Boolean, Column, DateTime
from sqlalchemy import Enum as EnumField
from sqlalchemy import Integer, String
from sqlalchemy.sql import func

from janusbackup.schemas import ConnectionType, DBType

from .base import BaseModel


class ProjectModel(BaseModel):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=250), unique=True, nullable=False)
    connection_type = Column(EnumField(ConnectionType))

    # Host
    host = Column(String(length=100), nullable=True)
    host_user = Column(String(length=250), nullable=True)
    host_password = Column(String(length=250), nullable=True)

    # DB
    connection_schema = Column(String(length=100), nullable=True)
    connection_params = Column(JSON, default={})

    db_type: DBType = Column(EnumField(ConnectionType), nullable=False)

    db_host = Column(String(length=100), nullable=True)
    db_port = Column(Integer, nullable=True)

    db_name = Column(String(length=250), nullable=True)
    db_username = Column(String(length=250), nullable=True)
    db_password = Column(String(length=250), nullable=True)

    db_uri = Column(String(length=250), nullable=True)

    # Other
    is_dockerized = Column(Boolean, default=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    last_backup_at = Column(DateTime, nullable=True)

    provider_params = Column(JSON, default={})
    command_execute_params = Column(JSON, default={})

    def __str__(self):
        return f"Project {self.title} ({self.id})"
