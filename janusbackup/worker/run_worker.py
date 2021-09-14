import asyncio
import time

import schedule

from janusbackup.logger import logger
from janusbackup.worker.manager import JobManager


def run_worker(config):
    logger.info("Starting scheduler")
    loop = asyncio.get_event_loop()

    scheduler = schedule.Scheduler()

    for job in JobManager.get_jobs():
        job.set_schedule_job(scheduler, loop, config=config)

    try:
        while True:
            scheduler.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.error("\nStopped manually with keyboard")

    return
