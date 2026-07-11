"""environment.py handler to read and write values"""

# use a .env file and place it into utils_xs root folder
import os
import re
import logging
import json
from typing import Optional, Literal, Union
from pathlib import Path
from dotenv import dotenv_values
from libs.helper import Helper, Persistence
from config.color_logger import setup_color_logging

# ensure root logger will use colored logger
setup_color_logging(use_color=True, use_emoji=True, indent=120)
logger = logging.getLogger(__name__)

# here's a definition of defined Environment values as Reference
# custom_print / CRITICAL,ERROR,WARNING,INFO,DEBUG
MY_ENV_PRINT_LEVEL = "MY_ENV_PRINT_LEVEL"

# setting the debug level
MY_ENV_DEBUG_LEVEL = "MY_ENV_DEBUG_LEVEL"

# path to a markdown test file markdown_parser
F_MARKDOWN_TEST = "F_MARKDOWN_TEST"

DEBUG_LEVEL: dict = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
}

UNSAFE = re.compile(r"[ \t#\$\\]|^\s|\s$")


class Environment:
    """Wrapper around Environment."""

    def __init__(self, env_dict: dict[str, Union[str, list]] = {}, f_dotenv: Optional[str] = None, as_env: bool = True):
        """Constructor.
        Also allows to pass list as environment values and will treat first element as value and the second one as comment

        """

        # get a path to a dotenv file
        # /utils_xs/src/libs
        self._f_dotenv: Path = (
            Path(f_dotenv).absolute()
            if f_dotenv is not None
            else Path(__file__).parent.parent.parent.joinpath(".env").absolute()
        )
        self._environment: dict = {}
        if not self._f_dotenv.is_file() and len(env_dict) == 0:
            logger.warning(f"Path [{self._f_dotenv}] is nto a valid path and no env values were supplied")

        # dictionary containing environment values
        self._env_dict: dict = env_dict

        # flag whether to set environment
        self._as_env: bool = as_env
        # environemnt values from dotenv file and from passed dictionary
        self._environment: dict = self._get_dotenv_values()
        self._environment.update(env_dict)
        # read the dotenv file
        self.create_environment()

    def _get_dotenv_values(self) -> dict:
        """read the environment variables"""
        out: dict = {}
        if not self._f_dotenv.is_file():
            return out
        out = dict(dotenv_values(self._f_dotenv))
        logger.debug(f"Values in dotenv environment [{self._f_dotenv}]\n{json.dumps(out, indent=4, default=str)}")

    def create_environment(self) -> None:
        """creates the environment variables"""
        if self._as_env is False:
            return

        for k, v in self._environment.items():
            if isinstance(v, str):
                os.environ[k] = v
            elif isinstance(v, list):  #
                if len(v) > 0:
                    os.environ[k] = v[0]
            else:
                os.environ[k] = str(v)

            logger.debug(f"Setting Environment {k:<20}: {v}")

    def _get_dotenv_quotes(self, value: str) -> str:
        """for dotenv files decide whether quotes should be used, returns the quotes"""
        if bool(UNSAFE.search(value)):
            return '"'
        else:
            return ""

    def save_environemnt(
        self, f_out: Union[str, Path], filetype: Literal["win", "sh", "text", "dotenv", "json"] = "text"
    ) -> None:
        """Saves the environment into a file (eiter as windows command file, linux shell,json, dotenv or as single files)"""
        # saving to a single or multiple files
        files_out: dict = {}
        out_lines: list[str] = []
        out_dict: dict = {}

        _f_out: Path = Path(f_out).absolute()
        if _f_out.is_dir() and filetype != "text":
            logger.error(f"Passed Filepath [{str(_f_out)}] is a path, supply path to a file")
            return None
        if not _f_out.parent.is_dir() and filetype != "text":
            logger.error(
                f"Parent Path of [{str(_f_out)}] is not a path, supply path to a file with a valid parent path"
            )
            return None
        elif filetype == "text" and not _f_out.is_dir():
            logger.error(f"[{str(_f_out)}] is not a path, supply a ath for environment files of type text")
            return None

        # get the comment character
        _comment_dict: dict = {"win": "rem", "sh": "#", "dotenv": "#", "text": "", "json": ""}
        _comment_prefix = _comment_dict.get(filetype, "")
        _title: str = f"Env Created using environment.py on {Helper.format_timestamp()}"
        if len(_comment_prefix) > 0:
            out_lines.append(f"{_comment_prefix} {_title}")

        for env_key, env_value in self._env_dict.items():
            _value: Optional[str] = None
            _comment: Optional[str] = None
            if isinstance(env_value, str):
                _value = env_value
            elif isinstance(env_value, list):
                if len(env_value) > 0:
                    _value = env_value[0]
                if len(env_value) > 1:
                    _comment = env_value[1]
            elif env_value is not None:
                _value = str(env_value)
            else:
                _value = ""

            # create comment if given
            if _comment and _comment_prefix:
                out_lines.append(f"{_comment_prefix} {_comment}")

            # depending on type add value
            if filetype == "win":
                out_lines.append(f'SET "{env_key}={_value}"')
            elif filetype == "sh":
                out_lines.append(f'SET "{env_key}={_value}"')
            elif filetype == "dotenv":
                _dotenv_quote = self._get_dotenv_quotes(env_value)
                out_lines.append(f"{env_key}={_dotenv_quote}{_value}{_dotenv_quote}")
            elif filetype == "text":
                # simply create a new file containing the value and filename
                files_out[f_out.joinpath(env_key.strip())] = _value.strip()
            elif filetype == "json":
                out_dict[env_key.strip()] = _value.strip()
            else:
                logger.warning(f"Invalid filetype [{filetype}] passed, skip creation of environment vlaue [{env_key}]")

        # now prepare the env values for saving
        if filetype == "json":
            Persistence.save_json(_f_out, out_dict)
        elif filetype == "text":
            for _file, _value in files_out.items():
                Persistence.save_txt(_file, str(_value).strip)
        else:
            Persistence.save_txt(_f_out, out_lines)

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

    @staticmethod
    def get_debug_level(default: str = "DEBUG") -> int:
        """Gets the debug level from env variable MY_ENV_DEBUG_LEVEL
        and sets a default level, if not found"""
        _debug_level_str = os.environ.get(MY_ENV_DEBUG_LEVEL)
        # if not in environemnt use passed value or default value
        if _debug_level_str is None:
            _debug_level_str = default.upper()

        # returns the debug level or predefined level
        return DEBUG_LEVEL.get(_debug_level_str.upper(), logging.debug)


if __name__ == "__main__":
    logger.setLevel(Environment.get_debug_level("DEBUG"))
    environment = Environment()
    environment.get("KKK")
    environment.get("HUGOTEST")
