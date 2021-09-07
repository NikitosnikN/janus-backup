from janusbackup.core.integrations import S3Wrapper
from janusbackup.core.mechanics.backup_providers import BackupProviderManager
from janusbackup.database.models import ProjectModel
from janusbackup.logger import logger
from janusbackup.schemas import ProjectSchema


class BackupPipeline:
    @classmethod
    async def run_pipeline(cls, provider):
        await provider.start_backup()

        if not provider.validate_backup_exists():
            raise ValueError("Failed to find backup file")

        with open(provider.backup_filepath, "rb") as file:
            async with S3Wrapper() as s3:
                await s3.upload_backup(
                    project_title=provider.project_title, backup_filename=provider.filename, file=file
                )

        # TODO delete local file if success upload
        # os.remove()

        logger.info(f"Project {provider.project_title} backup pipeline finished")
        return None

    @classmethod
    async def run_pipeline_for_schema(cls, project: ProjectSchema) -> None:
        logger.info(f"Project {project.title} backup pipeline started")
        provider_class = BackupProviderManager.get_provider_by_type(project.db_type)

        if not provider_class:
            raise ValueError(f"Provider class '{project.db_type}' not found")

        provider = provider_class.from_schema(project)
        return await cls.run_pipeline(provider)

    @classmethod
    async def run_pipeline_for_project(cls, project: ProjectModel) -> None:
        logger.info(f"Project {project.title} backup pipeline started")
        provider_class = BackupProviderManager.get_provider_by_type(project.db_type)

        if not provider_class:
            raise ValueError(f"Provider class '{project.db_type}' not found")

        provider = provider_class.from_project(project)

        return await cls.run_pipeline(provider)

    @classmethod
    async def start_pipeline(cls):
        logger.info("Backup pipeline started")

        projects = await ProjectModel.all()

        for project in projects:
            await cls.run_pipeline_for_project(project)

        logger.info("Backup pipeline finished")
        return None
