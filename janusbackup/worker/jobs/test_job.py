import asyncio

from schedule import Scheduler

from janusbackup.logger import logger
from janusbackup.worker.jobs import BaseJob


class TestJob(BaseJob):
    @staticmethod
    async def _job(*args, **kwargs):
        logger.info("Hello world")

    @classmethod
    def set_schedule_job(cls, scheduler: Scheduler, loop: asyncio.BaseEventLoop):
        scheduler.every(10).seconds.do(cls.get_schedule_job(), loop=loop)
