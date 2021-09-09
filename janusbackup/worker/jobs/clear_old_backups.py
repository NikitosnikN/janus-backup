import asyncio

from schedule import Scheduler

from janusbackup.worker.jobs import BaseJob


class ClearOldBackupsJob(BaseJob):
    is_active = False

    @staticmethod
    async def _job(*args, **kwargs):
        pass

    @classmethod
    def set_schedule_job(cls, scheduler: Scheduler, loop: asyncio.BaseEventLoop, *args, **kwargs):
        scheduler.every(1).minute.do(cls.get_schedule_job(), loop=loop)
