from asyncio import AbstractEventLoop
from datetime import datetime, timedelta

from janusbackup.core.utils import catch_exceptions
from janusbackup.database.models import LogModel
from janusbackup.logger import db_logger, logger
from janusbackup.schemas import LogDBPayload, LogType

__all__ = ["clear_logs_in_db_wrapper"]


async def clear_logs_in_db():
    result = await LogModel.filter(created_at__lte=(datetime.now() - timedelta(days=30))).delete()
    logger.info(f"Cleared {result} logs")
    db_logger.info("", exc_info={"payload": LogDBPayload(type=LogType.LOGS_DELETED, payload={"count": result})})
    return


@catch_exceptions(cancel_on_failure=False)
def clear_logs_in_db_wrapper(loop: AbstractEventLoop):
    loop.run_until_complete(clear_logs_in_db())
