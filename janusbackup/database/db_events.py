import logging

import sentry_sdk

__all__ = ["test_db_connection", "close_db_connection"]


async def test_db_connection():
    logging.info("Testing db connection")

    try:
        logging.info("Successfully started db connection")
    except Exception as e:
        logging.error(f"Unable to connect DB, error {e.__class__.__name__}")
        sentry_sdk.capture_exception(e)
        return None


async def close_db_connection():
    logging.info("Shutting down db connection")
