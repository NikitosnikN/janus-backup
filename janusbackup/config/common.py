from os import getenv, path

DEBUG = getenv("DEBUG", "") == "True"

if DEBUG:
    from dotenv import load_dotenv

    load_dotenv()

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

TITLE = getenv("TITLE", "janus-api")

VERSION = getenv("VERSION")
RELEASE = getenv("RELEASE")
COMMIT = getenv("COMMIT")
ENVIROMENT = getenv("ENV") or getenv("ENVIROMENT")

DOMAIN = getenv("DOMAIN")
HOST_URL = getenv("HOST_URL")

SECRET = getenv("SECRET", "87de177d-0add-4783-80e1-171dd133a035")
SECRET_FERNET = getenv("SECRET_FERNET", "MSEaI3ruv6KfGQu0mHSZaotQZfhHYB6NjJ0YxGC0lPw=")

API_HOST = getenv("API_HOST", "0.0.0.0")
API_PORT = getenv("API_PORT", 4000)

IS_PRODUCTION = ENVIROMENT == "production"
IS_STAGING = ENVIROMENT == "staging"
IS_DEVELOPMENT = ENVIROMENT == "develop"
IS_LOCAL = ENVIROMENT == "develop"

ALLOWED_ORIGINS = ["*"]

DEFAULT_BACKUP_PATH = getenv("DEFAULT_BACKUP_PATH", "")
