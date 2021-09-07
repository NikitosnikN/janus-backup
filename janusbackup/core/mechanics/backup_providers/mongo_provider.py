import asyncio
import json
import secrets
from enum import Enum
from typing import List, Optional
from urllib.parse import urlencode

from pydantic import Field
from sshtunnel import SSHTunnelForwarder

from janusbackup.config import DEFAULT_BACKUP_PATH
from janusbackup.core.mechanics.backup_providers import BaseBackupProvider
from janusbackup.database import DBType, ProjectModel
from janusbackup.schemas import BaseModel, ProjectSchema


class MongoParamsSchema(BaseModel):
    execute_path: str = Field(default="/usr/bin/mongodump")
    backup_extension: str = Field(default="gz")


class SSHConnectMode(str, Enum):
    user_password = "user_password"
    private_key = "private_key"

    @classmethod
    def get_names(cls) -> List[str]:
        return list(cls.__members__)


class MongoBackupProvider(BaseBackupProvider):
    db_type = DBType.MONGODB
    params_schema = MongoParamsSchema

    def __init__(
        self,
        connection_schema: str,
        db_host: str,
        db_port: int,
        db_username: str,
        db_password: str,
        db_name: str,
        connection_params: Optional[dict],
        backup_path: str,
        command_execute_params: Optional[List[str]] = None,
        project: Optional[ProjectModel] = None,
        project_title: Optional[str] = None,
        with_ssh_tunnel: bool = False,
        **kwargs,
    ):
        self._connection_schema = connection_schema
        self._db_host = db_host
        self._db_port = db_port
        self._db_username = db_username
        self._db_password = db_password
        self._db_name = db_name
        self._connection_params = connection_params

        self._backup_path = backup_path

        self._tunnel_host = None
        self._tunnel_port = None

        self._with_ssh_tunnel = with_ssh_tunnel
        self._ssh_connect_mode: SSHConnectMode = kwargs.get("ssh", {}).get("mode", SSHConnectMode.user_password.name)

        if self._ssh_connect_mode not in SSHConnectMode.get_names():
            raise ValueError(f"Invalid ssh connect mode name '{self._ssh_connect_mode}'")

        self._ssh_username = kwargs.get("ssh", {}).get("username")

        self._ssh_password = kwargs.get("ssh", {}).get("password")

        self._ssh_private_key_path = kwargs.get("ssh", {}).get("private_key_path")
        self._ssh_private_key_password = kwargs.get("ssh", {}).get("private_key_password")

        self._ssh_host = kwargs.get("ssh", {}).get("host")
        self._ssh_port = kwargs.get("ssh", {}).get("port", 22)
        self._ssh_remote_host = kwargs.get("ssh", {}).get("remote_host", self._ssh_host)
        self._ssh_remote_port = kwargs.get("ssh", {}).get("remote_port", self._db_port)

        self._ssh_tunnel: Optional[SSHTunnelForwarder] = None

        self._command_execute_params = command_execute_params or []

        self._project = project or None
        self.project_title = project_title or self._project.title if self._project else None
        self._task_id = secrets.token_urlsafe(5)

        self._kwargs = kwargs

        self._provider_params = {}

        self._generated_filename = None

    @property
    def _connection_uri(self):
        connection_params = ""

        if self._connection_params:
            connection_params = f"?{urlencode(self._connection_params)}"

        return (
            f"{self._connection_schema}://"
            f"{self._db_username}:{self._db_password}@"
            f"{self._tunnel_host or self._db_host}:{self._tunnel_port or self._db_port}/"
            f"{connection_params}"
        )

    @staticmethod
    def validate_result(result: bytes) -> bool:
        return not result

    async def _load_provider_params(self):
        provider_params = self._project.provider_params if self._project and self._project.provider_params else {}

        self._provider_params.update(self.params_schema(**provider_params).dict())

        return self._provider_params

    async def _execute_mongodump(self):
        command = [
            self._provider_params.get("execute_path"),
            "--uri",
            self._connection_uri,
            "--gzip",
            f"--archive={self.backup_filepath}",
        ]
        command.extend(self._command_execute_params)

        proc = await asyncio.create_subprocess_shell(
            " ".join(command),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        _, stderr = await proc.communicate()

        return stderr

    def _set_ssh_tunnel(self):
        credential_tunnel_params = {}

        if self._ssh_connect_mode == SSHConnectMode.user_password:
            credential_tunnel_params.update({"ssh_username": self._ssh_username, "ssh_password": self._ssh_password})

        elif self._ssh_connect_mode == SSHConnectMode.private_key:
            credential_tunnel_params.update(
                {
                    "ssh_username": self._ssh_username,
                    "ssh_private_key": self._ssh_private_key_path,
                    "ssh_private_key_password": self._ssh_private_key_password,
                }
            )

        if None in credential_tunnel_params.values():
            raise ValueError(
                f"Invalid ssh connect credentials for mode '{self._ssh_connect_mode}':\n"
                f"{json.dumps(credential_tunnel_params, indent=2)}"
            )

        self._ssh_tunnel = SSHTunnelForwarder(
            (self._ssh_host, int(self._ssh_port)),
            ssh_username=self._ssh_username,
            ssh_password=self._ssh_password,
            remote_bind_address=(self._ssh_remote_host, int(self._ssh_remote_port)),
        )

        self._ssh_tunnel.start()

        self._tunnel_port = self._ssh_tunnel.local_bind_port
        self._tunnel_host = self._ssh_tunnel.local_bind_host

    async def start_backup(self):
        await self._load_provider_params()

        self._generate_filename(self._task_id, self._provider_params["backup_extension"])

        if self._ssh_tunnel:
            self._set_ssh_tunnel()

        result = await self._execute_mongodump()

        if not self.validate_result(result):
            raise ValueError("Failed to backup db")

        if self._ssh_tunnel and self._ssh_tunnel.is_active:
            self._ssh_tunnel.close()

        return None

    @classmethod
    def from_project(cls, project: ProjectModel, **kwargs) -> "MongoBackupProvider":
        return cls(
            connection_schema=project.connection_schema,
            db_host=project.db_host,
            db_port=project.db_port,
            db_username=project.db_username,
            db_password=project.db_password,
            db_name=project.db_name,
            backup_path=DEFAULT_BACKUP_PATH,
            connection_params=project.connection_params,
            command_execute_params=project.command_execute_params,
            project=project,
            with_ssh_tunnel=project.use_ssh_tunnel,
            **kwargs,
        )

    @classmethod
    def from_schema(cls, project: ProjectSchema, **kwargs) -> "MongoBackupProvider":
        return cls(
            connection_schema=project.connection_schema,
            db_host=project.db_host,
            db_port=project.db_port,
            db_username=project.db_username,
            db_password=project.db_password,
            db_name=project.db_name,
            backup_path=DEFAULT_BACKUP_PATH,
            connection_params=project.connection_params,
            project_title=project.title,
            # command_execute_params=project.command_execute_params,
            # project=project,
            # with_ssh_tunnel=project.use_ssh_tunnel,
            **kwargs,
        )

    @classmethod
    async def init_and_start_backup(
        cls,
        connection_schema: str,
        db_host: str,
        db_port: str,
        db_username: str,
        db_password: str,
        db_name: str,
        connection_params: Optional[dict] = None,
        project: Optional[ProjectModel] = None,
        backup_path: str = DEFAULT_BACKUP_PATH,
        with_ssh_tunnel: bool = False,
        command_execute_params: Optional[List[str]] = None,
        **kwargs,
    ):
        obj = cls(
            connection_schema,
            db_host,
            db_port,
            db_username,
            db_password,
            db_name,
            connection_params,
            backup_path,
            command_execute_params,
            project,
            with_ssh_tunnel,
            **kwargs,
        )

        return await obj.start_backup()
