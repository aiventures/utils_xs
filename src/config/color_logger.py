"""color_logger.py colored logger output.
be sure to instancite the logger at first instanciation of a logger
"""

from datetime import datetime as DateTime
import logging
from enum import StrEnum
from config.colors import ESC, C_PY, C_I, C_W, C_E, COL_PINK_BRIGHT_198, COL_RESET, COL_BLUE_SKY, C_F

# Constants
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MSG_FORMAT = "%(asctime)-17s %(levelname)-20s %(module)s [%(name)s.%(funcName)s(%(lineno)d)] %(message)s"


class LOGGING_COLOR(StrEnum):
    """Logging Colors. As Enum Colors need to be Different"""

    DEBUG = C_PY
    INFO = C_I
    WARNING = C_W
    ERROR = C_E
    CRITICAL = COL_PINK_BRIGHT_198


class LOGGING_EMOJI(StrEnum):
    """Logging Emojis"""

    DEBUG = "💻"
    INFO = "🔵"
    WARNING = "🟡"
    ERROR = "🔴"
    CRITICAL = "🔥"


COL_LOG_LEVELS = [c.name for c in LOGGING_COLOR]


# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class ColoredFormattter(logging.Formatter):
    """Color Formatter"""

    def __init__(self, msg, use_color: bool = True, use_emoji: bool = False, indent: int = 180):
        logging.Formatter.__init__(self, msg, datefmt=DATE_FORMAT)
        self._use_color = use_color
        self._use_emoji = use_emoji
        self._indent: int = indent

    def formatTime(self, record, datefmt=None):
        dt = DateTime.fromtimestamp(record.created)
        timestamp = dt.strftime(DATE_FORMAT)
        return f"{COL_BLUE_SKY}{timestamp}{COL_RESET}"

    def format(self, record):
        message_unformatted = super().format(record)

        levelname: str = record.levelname.upper()
        _emoji: str = ""
        _msg: str = record.getMessage()
        _lineno_s = None
        if levelname in COL_LOG_LEVELS:
            if self._use_color and levelname in COL_LOG_LEVELS:
                _loglevel_color = LOGGING_COLOR[levelname].value
                _indent = (11 - len(levelname)) * " "
                # color the levelname
                _levelname_color = _loglevel_color + levelname + _indent + COL_RESET
                record.levelname = _levelname_color
                _msg = f"{_loglevel_color}{_msg}{COL_RESET}"
                # color the various parts of the message
                record.name = f"{COL_BLUE_SKY}{record.name}{COL_RESET}"
                record.funcName = f"{COL_BLUE_SKY}{record.funcName}{COL_RESET}"
                _lineno_s = f"({str(record.lineno)})"
                record.module = f"{C_F}{record.module}{COL_RESET}"
                record.filename = f"{C_F}{record.filename} hugo{COL_RESET}"

            if self._use_emoji:
                _emoji = f"{LOGGING_EMOJI[levelname].value} "
            _msg = f"{_emoji}{_msg}"

        record.msg = _msg
        _message = logging.Formatter.format(self, record)
        # replace some additional fields
        if _lineno_s:
            _message = _message.replace(_lineno_s, f"{C_W}{_lineno_s}{COL_RESET}")
        # split at the first ] symbol and realign the last part (message) if applicable
        if self._indent > 0:
            message_parts_unformatted = message_unformatted.split("]", 1)
            indent = ""
            if len(message_parts_unformatted[0]) < self._indent:
                indent = " " * (self._indent - len(message_parts_unformatted[0]))
                message_parts = _message.split("]", 1)
                _message = f"{message_parts[0]}]{indent}{message_parts[1]}"

        return f"{_emoji}{_message}"


def setup_color_logging(level=logging.DEBUG, use_color: bool = True, use_emoji: bool = True, indent: int = 100):
    """make sure root hanlder will use colored fomratter"""
    root = logging.getLogger()
    if root.handlers:
        return  # Prevent duplicate handlers if called twice

    _formatter = ColoredFormattter(MSG_FORMAT, use_color, use_emoji, indent)
    _console = logging.StreamHandler()
    _console.setFormatter(_formatter)
    root.addHandler(_console)
    root.setLevel(level)


# Testing the Logger
if __name__ == "__main__":
    setup_color_logging(use_color=True, use_emoji=True)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug("DEBUG MESSAGE")
    logger.info("INFO MESSAGE")
    logger.warning("WARNING MESSAGE")
    logger.error("ERROR MESSAGE")
    logger.fatal("FATAL MESSAGE")
