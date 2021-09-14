import asyncio
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import Any, Callable, Coroutine

from schedule import Scheduler

from janusbackup.core.utils import catch_exceptions


def async_job_starter(f: Callable[[Any, Any], Coroutine], cancel_on_failure: bool = True):
    @catch_exceptions(cancel_on_failure=cancel_on_failure)
    def wrapper(loop: AbstractEventLoop, *args, **kwargs):
        loop.run_until_complete(f(*args, **kwargs))

    return wrapper


class BaseJob(ABC):
    name: str
    is_active: bool = True
    cancel_on_failure: bool = True

    @staticmethod
    @abstractmethod
    async def _job(*args, **kwargs):
        pass

    @classmethod
    def get_schedule_job(cls):
        if asyncio.iscoroutinefunction(cls._job):
            return async_job_starter(cls._job, cls.cancel_on_failure)

        return cls._job

    @classmethod
    @abstractmethod
    def set_schedule_job(cls, scheduler: Scheduler, loop: asyncio.BaseEventLoop, *args, **kwargs):
        pass
