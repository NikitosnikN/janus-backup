import asyncio
import secrets
from typing import Tuple
from urllib.parse import urlencode

from pydantic import Field

from janusbackup.config import Config
from janusbackup.core.backup_providers import BaseBackupProvider
from janusbackup.database import DBType
from janusbackup.schemas import BaseModel, ProjectSchema


class MongoParamsSchema(BaseModel):
    execute_path: str = Field(default="/usr/bin/mongodump")
    backup_extension: str = Field(default="gz")


class MongoBackupProvider(BaseBackupProvider):
    connection_schema: str = "mongodb"
    db_type = DBType.MONGODB
    params_schema = MongoParamsSchema

    def __init__(self, project: ProjectSchema, config: Config = None, **kwargs):
        super().__init__(project, config, **kwargs)

        self._task_id = secrets.token_urlsafe(5)
        self._provider_params = {}

    @property
    def _connection_uri(self) -> str:
        uri = (
            f"{self.connection_schema}://"
            f"{self.project.db_username}:{self.project.db_password}@"
            f"{self.project.db_host}:{self.project.db_port}/"
        )

        if self.project.connection_params:
            uri += f"?{urlencode(self.project.connection_params)}"

        return uri

    def _build_command(self) -> str:
        command = [
            self._provider_params["execute_path"],
            "--uri",
            self._connection_uri,
            "--gzip",
            f"--archive={self.backup_filepath}",
        ]
        return " ".join(command)

    def _validate_results(self, stdout: bytes, stderr: bytes) -> None:
        pass

    async def _load_provider_params(self) -> dict:
        provider_params = self.project.provider_params if self.project and self.project.provider_params else {}
        self._provider_params.update(self.params_schema(**provider_params).dict())
        return self._provider_params

    async def _execute_mongodump(self) -> Tuple[bytes, bytes]:
        proc = await asyncio.create_subprocess_shell(
            self._build_command(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        return stdout, stderr

    #
    # def _set_ssh_tunnel(self):
    #     credential_tunnel_params = {}
    #
    #     if self._ssh_connect_mode == SSHConnectMode.user_password:
    #         credential_tunnel_params.update({"ssh_username": self._ssh_username, "ssh_password": self._ssh_password})
    #
    #     elif self._ssh_connect_mode == SSHConnectMode.private_key:
    #         credential_tunnel_params.update(
    #             {
    #                 "ssh_username": self._ssh_username,
    #                 "ssh_private_key": self._ssh_private_key_path,
    #                 "ssh_private_key_password": self._ssh_private_key_password,
    #             }
    #         )
    #
    #     if None in credential_tunnel_params.values():
    #         raise ValueError(
    #             f"Invalid ssh connect credentials for mode '{self._ssh_connect_mode}':\n"
    #             f"{json.dumps(credential_tunnel_params, indent=2)}"
    #         )
    #
    #     self._ssh_tunnel = SSHTunnelForwarder(
    #         (self._ssh_host, int(self._ssh_port)),
    #         ssh_username=self._ssh_username,
    #         ssh_password=self._ssh_password,
    #         remote_bind_address=(self._ssh_remote_host, int(self._ssh_remote_port)),
    #     )
    #
    #     self._ssh_tunnel.start()
    #
    #     self._tunnel_port = self._ssh_tunnel.local_bind_port
    #     self._tunnel_host = self._ssh_tunnel.local_bind_host

    async def start_backup(self) -> None:
        await self._load_provider_params()

        self._generate_filename(self._task_id, self._provider_params["backup_extension"])

        out, err = await self._execute_mongodump()

        self._validate_results(out, err)

        return None
