import logging
import sys

from janusbackup.config import IS_LOCAL

__all__ = ["logger", "tg_logger"]

logger = logging.getLogger("janus-backups")

logger.addHandler(logging.StreamHandler(sys.stdout))

tg_logger = logging.getLogger("janus-backup-tg")

if IS_LOCAL:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
