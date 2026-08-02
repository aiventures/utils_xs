"""Custom Print Command to supply preformatted print output"""

import os
import json
from typing import Optional
from datetime import datetime as DateTime

# ANSI color codes
from config.colors import colorize

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
    "CRITICAL": "C_E",
    "ERROR": "C_E",
    "WARNING": "C_W",
    "INFO": "C_I",
    "DEBUG": "C_PY",
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


def printcol(s: str, c: str = "", e: Optional[str] = "", reset_col: str = "C_0") -> Optional[str]:
    """Custom Color Print statement including emoji"""
    if s is None:
        return
    e_ = "" if e is None else f"{e} "
    s_ = f"{e_}{colorize(s, c, reset_col)}"
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
    d: dict, title: Optional[str] = None, lf: bool = False, debuglevel: str = "INFO", col_json: str = "C_PY"
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
        printcol(title, "C_T", emoji)
    printcol(data, col_json)
    return data


def inputc(s: str) -> str:
    """user input"""
    if s is None:
        return
    s_ = f"{colorize(s, 'C_Q'), False} {colorize('>', 'C_F')} "
    return input(s_)


def printt(s: str) -> str:
    """print title"""
    e = "🧿" if get_print_show_emoji() else None
    return printcol(s, "C_T", e)


def printh(s: str) -> str:
    """print highlight"""
    s_ = colorize(s, "C_H")
    print(s)
    return s_


def printpy(s: str) -> str:
    """print code"""
    s_ = colorize(s, "C_PY")
    print(s)
    return s_


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


def print_infoline(
    text: str,
    index: Optional[int] = None,
    line_number: Optional[int] = None,
    num_digits: int = 4,
    date: Optional[str] = None,
    contexts: Optional[list | str] = None,
    search_matches: Optional[list | str] = None,
    breadcrumb: Optional[str] = None,
    text_length: Optional[int] = None,
    show: bool = True,
) -> str:
    """prints a colored information line in a standardized way."""
    out: str = ""
    # add collateral items
    i_ = colorize(f"{str(index).zfill(num_digits)} ", "C_SI") if index else ""
    l_ = colorize(f"L{str(line_number).zfill(num_digits)} ", "C_L") if line_number else ""
    d_ = f"{colorize(f'[{date}]', 'C_D')} " if date else ""
    c_ = ",".join(contexts) if isinstance(contexts, list) else contexts
    c_ = f"{colorize(f'{c_}', 'C_C')} " if c_ else ""
    t_ = colorize(f"{text.strip()} ", "C_TX")
    b_ = "" if breadcrumb is None else colorize(f"[{breadcrumb}] ", "C_BR")
    # finally colorize any search hits in the text
    if search_matches:
        matches_ = search_matches if isinstance(search_matches, list) else [search_matches]
    else:
        matches_ = []

    t_ = t_.strip()
    for m in matches_:
        t_ = t_.replace(m, colorize(m, "C_M", "C_TX"))
    # fill up text with spaces
    if text_length and len(t_) < text_length:
        s_ = (text_length - len(t_)) * " "
        t_ = f"{t_}{s_}"
    out = f"{i_}{l_}{d_}{t_} {b_}{c_}".strip()
    if show:
        print(out)
    return out


if __name__ == "__main__":
    """ testdrive  """
    set_print_level("INFO", show_emoji=True)
    printt("X ### LEVEl INFO ")
    printd("DEBUG MESSAGE")
    printi("INFO MESSAGE")
    printw("WARNING MESSAGE")
    printe("ERROR MESSAGE")
    printc("CRITICAL MESSAGE")
    set_print_level("DEBUG", show_emoji=True)
    printt("Y ### LEVEl DEBUG ")
    printd("DEBUG MESSAGE")
    printi("INFO MESSAGE")
    printw("WARNING MESSAGE")
    printe("ERROR MESSAGE")
    printc("CRITICAL MESSAGE")
    # checking the print of an information line
    print_infoline(
        text="hugo ist ein schelm",
        index=43,
        line_number=440,
        num_digits=3,
        date="2026/07/01",
        contexts=["@context1"],
        search_matches=["ist"],
        breadcrumb="A>B>C",
        text_length=80,
        show=True,
    )

    print_infoline(
        text="hugo ist ein schelm nummer2",
        line_number=440,
        num_digits=3,
        search_matches=["ist"],
        breadcrumb="A>B>C",
        text_length=50,
        show=True,
    )

    pass
