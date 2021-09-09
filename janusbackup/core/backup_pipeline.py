import time

from janusbackup.config import CONFIG_FACTORY, Config
from janusbackup.core.backup_providers import BackupProviderManager
from janusbackup.core.integrations import S3Wrapper
from janusbackup.core.utils import ProjectsLoader
from janusbackup.logger import logger
from janusbackup.schemas import ProjectSchema


class BackupPipeline:
    def __init__(self, config: Config = None) -> None:
        self.config = config or CONFIG_FACTORY()

    def _get_provider_class(self, project: ProjectSchema):
        provider_class = BackupProviderManager.get_provider_by_type(project.db_type)

        if not provider_class:
            raise ValueError(f"Provider class '{project.db_type}' not found")

        return provider_class(project=project, config=self.config)

    async def _load_backup_to_storage(self, provider) -> None:
        with open(provider.backup_filepath, "rb") as file:
            async with S3Wrapper(self.config) as s3:
                await s3.upload_backup(
                    project_title=provider.project.title,
                    backup_filename=provider.filename,
                    file=file,
                )

        return None

    async def run_pipeline(self, project: ProjectSchema):
        provider = self._get_provider_class(project)

        await provider.start_backup()

        if not provider.validate_backup_exists():
            raise ValueError("Failed to find backup file")

        await self._load_backup_to_storage(provider)

        provider.remove_backup()

        logger.info(f"Project {provider.project.title} backup pipeline finished")
        return None

    async def start_pipeline(self):
        logger.info("Backup pipeline started")

        t0 = time.time()

        projects = await ProjectsLoader(self.config).load()

        for project in projects:
            await self.run_pipeline(project)

        logger.info(f"Backup pipeline finished in {round(time.time() - t0, 4)}")
        return None
