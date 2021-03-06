import asyncio

from schedule import Scheduler

from janusbackup.logger import logger
from janusbackup.worker.jobs import BaseJob


class TestJob(BaseJob):
    is_active = False

    @staticmethod
    async def _job(*args, **kwargs):
        logger.debug("Hello world for TestJob")

    @classmethod
    def set_schedule_job(cls, scheduler: Scheduler, loop: asyncio.BaseEventLoop, *args, **kwargs):
        scheduler.every(5).seconds.do(cls.get_schedule_job(), loop=loop, *args, **kwargs)
