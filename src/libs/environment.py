"""environment.py handler to read and write values"""

# use a .env file and place it into utils_xs root folder
import os
from dotenv import dotenv_values
from typing import Optional, Literal
from pathlib import Path
import logging
import json

from config.color_logger import setup_color_logging

# ensure root logger will use colored logger
setup_color_logging(use_color=True, use_emoji=True, indent=120)
logger = logging.getLogger(__name__)

# here's a definition of defined Environment values as Reference
# custom_print / CRITICAL,ERROR,WARNING,INFO,DEBUG
MY_ENV_PRINT_LEVEL = "MY_ENV_PRINT_LEVEL"

# path to a markdown test file markdown_parser
F_MARKDOWN_TEST = "F_MARKDOWN_TEST"


class Environment:
    def __init__(self, f_dotenv: Optional[str] = None, as_env: bool = True):
        """Constructor."""

        # get a path to a dotenv file
        # /utils_xs/src/libs
        self._f_dotenv: Path = (
            Path(f_dotenv).absolute()
            if f_dotenv is not None
            else Path(__file__).parent.parent.parent.joinpath(".env").absolute()
        )
        self._environment: dict = {}
        if not self._f_dotenv.is_file():
            logger.error(f"Path [{self._f_dotenv}] is nto a valid path")
            return

        # flag whether to set environment
        self._as_env: bool = as_env
        # environemnt values
        self._environment: dict = {}
        # read the dotenv file
        self._get_dotenv_values()
        self.create_environment()

    def _get_dotenv_values(self) -> None:
        """read the environment variables"""
        self._environment = dict(dotenv_values(self._f_dotenv))
        logger.debug(f"Values in environment\n{json.dumps(self._environment, indent=4, default=str)}")

    def create_environment(self) -> None:
        """creates the environment variables"""
        if self._as_env is False:
            return
        for k, v in self._environment.items():
            os.environ[k] = str(v)
            logger.debug(f"Setting Environment {k:<20}: {v}")

    def get(
        self,
        key: str,
        default: Optional[str] = None,
        check: Literal["path", "file", "pathobject", "nocheck"] = "nocheck",
    ) -> Optional[str]:
        """retrieves environment value from environment"""
        v: Optional[str] = self._environment.get(key)
        if v is None:
            logger.warning(f"Environment key [{key}] is not defined")
            return default
        # check whether string is a valid path object
        error: Optional[str] = None
        if check == "file" and not Path(v).is_file():
            error = f"Environment [{key}]: {v} is not a valid path to a file"
        elif check == "path" and not Path(v).is_dir():
            error = f"Environment [{key}]: {v} is not a valid path to a directory"
        elif check == "pathobject" and not (Path(v).is_file() or Path(v).is_dir()):
            error = f"Environment [{key}]: {v} is not a valid path to a path object"
        if error:
            logger.error(error)
            return default

        return v


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    environment = Environment()
    environment.get("KKK")
    environment.get("HUGOTEST")
