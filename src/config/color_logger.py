"""color_logger.py colored logger output.
be sure to instancite the logger at first instanciation of a logger
"""

import logging
from enum import StrEnum
from config.colors import ESC, C_PY, C_I, C_W, C_E, COL_PINK_BRIGHT_198, COL_RESET

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

    def __init__(self, msg, use_color: bool = True, use_emoji: bool = False):
        logging.Formatter.__init__(self, msg, datefmt=DATE_FORMAT)
        self._use_color = use_color
        self._use_emoji = use_emoji

    def format(self, record):
        levelname: str = record.levelname.upper()
        _emoji: str = ""
        _msg: str = record.getMessage()
        if levelname in COL_LOG_LEVELS:
            if self._use_color and levelname in COL_LOG_LEVELS:
                _loglevel_color = LOGGING_COLOR[levelname].value
                _indent = (11 - len(levelname)) * " "
                _levelname_color = _loglevel_color + levelname + _indent + COL_RESET
                record.levelname = _levelname_color
                _msg = f"{_loglevel_color}{_msg}{COL_RESET}"
            if self._use_emoji:
                _emoji = f"{LOGGING_EMOJI[levelname].value} "
            _msg = f"{_emoji}{_msg}"
        record.msg = _msg
        return logging.Formatter.format(self, record)


# Custom Logger with multiple destinations
class ColoredLogger(logging.Logger):
    """Custom Logger to support colors"""

    def __init__(self, name):
        """Constructor"""
        logging.Logger.__init__(self, name, logging.DEBUG)
        _color_formatter = ColoredFormattter(MSG_FORMAT, use_color=True, use_emoji=True)
        _console = logging.StreamHandler()
        _console.setFormatter(_color_formatter)
        self.addHandler(_console)
        return


# Testing the Logger
if __name__ == "__main__":
    logging.setLoggerClass(ColoredLogger)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug("DEBUG MESSAGE")
    logger.info("INFO MESSAGE")
    logger.warning("WARNING MESSAGE")
    logger.error("ERROR MESSAGE")
    logger.fatal("FATAL MESSAGE")
