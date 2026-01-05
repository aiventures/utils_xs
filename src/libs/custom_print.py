"""Custom Print Command to supply preformatted print output"""

import os
import json
from typing import Optional

# ANSI color codes
from config.colors import C_0, C_E, C_I, C_PY, C_W, C_T, C_H, C_Q, C_F

MY_ENV_PRINT_LEVEL: str = "MY_PRINT_LEVEL"
MY_ENV_PRINT_SHOW_EMOJI: str = "MY_PRINT_SHOW_EMOJI"

PRINT_LEVELS: dict = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}

PRINT_LEVELS_EMOJIS: dict = {
    "CRITICAL": "🔥",
    "ERROR": "🚨",
    "WARNING": "🟨",
    "INFO": "🟦",
    "DEBUG": "🟩",
}

PRINT_LEVELS_COLOR: dict = {
    "CRITICAL": f"{C_E}",
    "ERROR": f"{C_E}",
    "WARNING": f"{C_W}",
    "INFO": f"{C_I}",
    "DEBUG": f"{C_PY}",
}


def get_print_show_emoji() -> bool:
    """get the setting whether emojis are shown"""
    return True if os.environ.get(MY_ENV_PRINT_SHOW_EMOJI, "").lower() == "true" else False


def set_print_show_emoji(show_emoji: bool) -> bool:
    """set the setting whether emojis are shown"""
    os.environ[MY_ENV_PRINT_SHOW_EMOJI] = str(show_emoji)


def get_print_level() -> int:
    """print level as int"""
    _level_env = os.environ.get("MY_PRINT_LEVEL", "INFO")
    _level_env = _level_env if _level_env in list(PRINT_LEVELS.keys()) else "INFO"
    return PRINT_LEVELS[_level_env]


def set_print_level(printlevel: str, show_emoji: bool = False) -> None:
    """setting the printing debug level"""
    level = printlevel if printlevel in list(PRINT_LEVELS.keys()) else "INFO"
    os.environ[MY_ENV_PRINT_LEVEL] = level
    set_print_show_emoji(show_emoji)


DEFAULT_LOG_LEVEL: int = get_print_level()


def is_printlevel(level: str) -> bool:
    """checks whether item should be printed"""
    level_int: int = PRINT_LEVELS.get(level, PRINT_LEVELS["INFO"])
    return True if (level_int >= get_print_level()) else False


def get_printlevel_emoji(level: str) -> Optional[str]:
    """ " gets an emoji depending from level"""
    if get_print_show_emoji() is False:
        return
    level_ = level if level in list(PRINT_LEVELS_EMOJIS.keys()) else "INFO"
    return PRINT_LEVELS_EMOJIS[level_]


def printcol(s: str, c: str = C_0, e: Optional[str] = "") -> Optional[str]:
    """Custom Color Print statement including emoji"""
    if s is None:
        return
    e_ = "" if e is None else f"{e} "
    s_ = f"{e_}{c}{s}{C_0}"
    print(s_)
    return s_


def print_level(s: str, level: str) -> Optional[str]:
    """prints string depending on level"""
    if s is None:
        return None
    s_ = s
    level_ = level if level in list(PRINT_LEVELS.keys()) else "INFO"
    level_int = PRINT_LEVELS.get(level_)
    printlevel_int = get_print_level()
    # do not print line
    if level_int < printlevel_int:
        return None
    show_emoji = get_print_show_emoji()
    color = PRINT_LEVELS_COLOR[level_]
    emoji = None
    if show_emoji:
        emoji = PRINT_LEVELS_EMOJIS[level_]
    s_ = printcol(s_, color, emoji)


def print_json(
    d: dict, title: Optional[str] = None, lf: bool = False, debuglevel: str = "INFO", col_json: str = C_PY
) -> Optional[str]:
    """default printout of dictionaries"""
    if not isinstance(d, dict):
        return

    # only show if minimum debug level is matched
    if PRINT_LEVELS.get(debuglevel, PRINT_LEVELS["INFO"]) < get_print_level():
        return

    if lf:
        print("\n")
    data = json.dumps(d, indent=4, ensure_ascii=False, default=str)
    if title is not None:
        emoji = "🔢" if get_print_show_emoji() else None
        printcol(title, C_T, emoji)
    printcol(data, col_json)
    return data


def inputc(s: str) -> str:
    """user input"""
    if s is None:
        return
    s_ = f"{C_Q}{s}{C_F}> {C_0}"
    return input(s_)


def printt(s: str) -> str:
    """print title"""
    e = "🧿" if get_print_show_emoji() else None
    return printcol(s, C_T, e)


def printh(s: str) -> str:
    """print highlight"""
    return f"{C_H}{s}{C_0}"


def printpy(s: str) -> str:
    """print code"""
    return f"{C_PY}{s}{C_0}"


def printd(s: str) -> Optional[str]:
    """print debug level"""
    return print_level(s, "DEBUG")


def printi(s: str) -> Optional[str]:
    """print info level"""
    return print_level(s, "INFO")


def printw(s: str) -> Optional[str]:
    """print warning level"""
    return print_level(s, "WARNING")


def printe(s: str) -> Optional[str]:
    """print error level"""
    return print_level(s, "ERROR")


def printc(s: str) -> Optional[str]:
    """print crtitical level"""
    return print_level(s, "CRITICAL")


if __name__ == "__main__":
    """ testdrive  """
    set_print_level("INFO", show_emoji=True)
    printt("### LEVEl INFO ")
    printd("DEBUG MESSAGE")
    printi("INFO MESSAGE")
    printw("WARNING MESSAGE")
    printe("ERROR MESSAGE")
    printc("CRITICAL MESSAGE")
    set_print_level("DEBUG", show_emoji=True)
    printt("### LEVEl DEBUG ")
    printd("DEBUG MESSAGE")
    printi("INFO MESSAGE")
    printw("WARNING MESSAGE")
    printe("ERROR MESSAGE")
    printc("CRITICAL MESSAGE")

    pass
