from os import getenv

import sentry_sdk

from .common import COMMIT, ENVIROMENT

__all__ = ["SENTRY_DSN"]

SENTRY_DSN = getenv("SENTRY_DSN", "")

if ENVIROMENT != "local":
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIROMENT,
        release=COMMIT,
    )
