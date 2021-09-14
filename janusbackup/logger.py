import logging.config
import sys

__all__ = ["logger"]

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"default": {"class": "logging.Formatter", "format": "%(asctime)s %(levelname)s %(message)s"}},
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "sys.stdout",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "janusbackup": {"handlers": ["default"], "level": "DEBUG"},
        "janusbackup.error": {"handlers": ["default"], "level": "INFO"},
        "janusbackup.notify": {"handlers": ["default"], "level": "INFO"},
    },
}

logger = logging.getLogger("janusbackups")
logger.setLevel("DEBUG")
logger.addHandler(logging.StreamHandler(sys.stdout))
