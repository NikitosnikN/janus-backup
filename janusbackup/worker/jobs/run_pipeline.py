import asyncio

from schedule import Scheduler

from janusbackup.core import BackupPipeline
from janusbackup.worker.jobs import BaseJob


class RunPipelineJob(BaseJob):
    @staticmethod
    async def _job(*args, **kwargs) -> None:
        await BackupPipeline(config=kwargs.get("config")).start_pipeline()

    @classmethod
    def set_schedule_job(cls, scheduler: Scheduler, loop: asyncio.BaseEventLoop, *args, **kwargs):
        scheduler.every(5).seconds.do(cls.get_schedule_job(), loop=loop, *args, **kwargs)
