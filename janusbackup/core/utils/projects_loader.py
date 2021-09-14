import json
from pathlib import Path
from typing import List, Union

import toml
import yaml
from pydantic import ValidationError

from janusbackup.config import CONFIG_FACTORY, Config
from janusbackup.logger import logger
from janusbackup.schemas import ProjectSchema


class ProjectsLoader:
    def __init__(self, config: Config = None):
        self.config = config or CONFIG_FACTORY()

    def _load_from_file(self) -> Union[list, dict]:
        path = Path(self.config.PROJECTS_SETTINGS_FILEPATH)
        extension = path.suffix

        with path.open("r") as f:
            if extension == ".json":
                data = json.load(f)["projects"]

            elif extension in (".yml", ".yaml"):
                data = yaml.load(f)["projects"]

            elif extension == ".toml":
                data = toml.load(f)["projects"]

            else:
                raise NotImplementedError(f".{extension} if not supported yet")

        return data

    async def load(self) -> List[ProjectSchema]:
        raw_data = self._load_from_file()
        try:
            data = [ProjectSchema(**i) for i in raw_data]
        except ValidationError as e:
            logger.error("Failed to load projects data")
            raise e

        return data
