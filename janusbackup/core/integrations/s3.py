import aioboto3

from janusbackup.config import CONFIG_FACTORY, Config

__all__ = ["S3Wrapper"]


class S3Wrapper:
    def __init__(self, config: Config = None):
        self.config = config or CONFIG_FACTORY()
        self.s3 = None
        self.bucket = None

    async def __aenter__(self):
        if not self.s3:
            self.s3 = await aioboto3.resource(
                "s3",
                endpoint_url=self.config.S3_URL,
                aws_access_key_id=self.config.S3_ACCESS_KEY,
                aws_secret_access_key=self.config.S3_SECRET_KEY,
            ).__aenter__()

        if not self.bucket:
            self.bucket = await self.s3.Bucket(self.config.S3_BUCKET)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.s3:
            await self.s3.__aexit__(exc_type, exc_val, exc_tb)
        return

    async def get_project_backups(self, project_title: str) -> list:
        objects = []
        async for s3_object in self.bucket.objects.filter(Prefix=project_title):
            objects.append(s3_object)

        return objects

    async def upload_backup(self, project_title: str, backup_filename: str, file) -> None:
        await self.bucket.put_object(Body=file, Key=f"{project_title}/{backup_filename}")

        return None

    async def remove_backup(self) -> None:
        pass
