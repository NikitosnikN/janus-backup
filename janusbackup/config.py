from typing import Optional

from dynaconf import Dynaconf, Validator

MODE_CHOICES = ("worker", "api")
CONFIG_TYPE_CHOICES = ("file", "env")


class Config(Dynaconf):
    pass


class ConfigFactory:
    def __init__(self):
        self._config = None

    def __call__(self, *args, **kwargs) -> Config:
        return self._config

    def get(self) -> Config:
        return self._config

    def set(self, config: Config):
        self._config = config


CONFIG_FACTORY = ConfigFactory()


def initialize_config(config_type: str, config_path: Optional[str]) -> Dynaconf:
    config = Config(
        envvar_prefix="",
        settings_file=config_path,
        load_dotenv=True,
        validators=[
            Validator("DEBUG", default=False, cast=bool),
            Validator("ENV", default="development", cast=str),
            Validator("SECRET", required=True, cast=str),
            Validator("PROJECTS_SETTINGS_FILEPATH", required=True, cast=str),
            Validator("S3_URL", required=True, cast=str),
            Validator("S3_ACCESS_KEY", required=True, cast=str),
            Validator("S3_SECRET_KEY", required=True, cast=str),
            Validator("S3_BUCKET", required=True, cast=str),
        ],
    )
    CONFIG_FACTORY.set(config)
    return config
