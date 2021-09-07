import asyncio
import time

import schedule

from janusbackup.logger import logger
from janusbackup.worker.jobs import clear_logs_in_db_wrapper
from janusbackup.worker.manager import JobManager


def run_worker():
    logger.info("Starting scheduler")
    loop = asyncio.get_event_loop()

    scheduler = schedule.Scheduler()

    jobs = JobManager.get_jobs()

    for job in jobs:
        job.set_schedule_job(scheduler, loop)

    scheduler.every(1).day.do(clear_logs_in_db_wrapper, loop=loop)

    try:
        while True:
            scheduler.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.error("Stopped manually with keyboard")

    return
