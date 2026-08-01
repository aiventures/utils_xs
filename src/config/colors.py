"""
Date of generation: 2026-01-12 08:59:47
"""

from typing import Optional

# Auto-generated from batch color definitions
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# Set background color	Next arguments are 48;5;<n> or 2;<r>;<g>;<b> (Default 49)
# Set foreground color	Next arguments are 38;5;<n> or 2;<r>;<g>;<b>, see below (Default 39)
ESC = "\033"
COL_BOLD = f"{ESC}[1m"
COL_UNDERLINE = f"{ESC}[4m"
COL_STRIKETHROUGH = f"{ESC}[9m"
COL_RESET = f"{ESC}[0m"
COL_RESET_BG = f"{ESC}[49m"
NUM_ARGS_COLORS = "0"
COL_TEST = f"{ESC}[38;2;229,229;229m"
COL_GREEN_DARK = f"{ESC}[38;5;34m"
COL_GREEN_LIGHT = f"{ESC}[38;5;46m"
COL_ORANGE_DARK = f"{ESC}[38;5;202m"
COL_ORANGE = f"{ESC}[38;5;208m"
COL_ORANGE_LIGHT = f"{ESC}[38;5;214m"
COL_YELLOW_LIGHT = f"{ESC}[38;5;226m"
COL_PINK = f"{ESC}[38;5;206m"
COL_PINK_LIGHT = f"{ESC}[38;5;212m"
COL_BLUE_DARK = f"{ESC}[38;5;33m"
COL_BLUE_LIGHT = f"{ESC}[38;5;45m"
COL_BLUE_SKY = f"{ESC}[38;5;75m"
COL_PURPLE_LIGHT = f"{ESC}[38;5;105m"
COL_GREY_DARK = f"{ESC}[38:5:242m"
COL_GREY_LIGHT = f"{ESC}[38;5;249m"
COL_DEFAULT = f"{ESC}[0m"
COL_RED = f"{ESC}[1;31;40m"
COL_GREEN = f"{ESC}[1;32;40m"
COL_YELLOW = f"{ESC}[1;33;40m"
COL_BLUE = f"{ESC}[1;34;40m"
COL_PURPLE = f"{ESC}[1;35;40m"
COL_LIGHTBLUE = f"{ESC}[1;36;40m"
COL_WHITE = f"{ESC}[1;37;40m"
COL_DEFAULT_BG = f"{ESC}[1;37;47m"
COL_RED_BG = f"{ESC}[1;31;41m"
COL_GREEN_BG = f"{ESC}[1;37;42m"
COL_YELLOW_BG = f"{ESC}[1;37;43m"
COL_BLUE_BG = f"{ESC}[1;37;44m"
COL_PURPLE_BG = f"{ESC}[1;37;45m"
COL_LIGHTBLUE_BG = f"{ESC}[1;37;46m"
COL_WHITE_BG = f"{ESC}[1;37;47m"
COL_GREY_WH = f"{ESC}[1;30;47m"
COL_RED_WH = f"{ESC}[1;31;47m"
COL_GREEN_WH = f"{ESC}[1;32;47m"
COL_YELLOW_WH = f"{ESC}[1;33;47m"
COL_BLUE_WH = f"{ESC}[1;34;47m"
COL_PURPLE_WH = f"{ESC}[1;35;47m"
COL_LIGHTBLUE_WH = f"{ESC}[1;36;47m"
COL_BLACK_WH = f"{ESC}[1;30;47m"
COL_RED_BRIGHT_196 = f"{ESC}[38;5;196m"
COL_RED_STRAWBERRY_204 = f"{ESC}[38;5;204m"
COL_ORANGE_RED_202 = f"{ESC}[38;5;202m"
COL_ORANGE_214 = f"{ESC}[38;5;214m"
COL_ORANGE_LIGHT_215 = f"{ESC}[38;5;215m"
COL_YELLOWGREEN_191 = f"{ESC}[38;5;191m"
COL_YELLOW_PALE_229 = f"{ESC}[38;5;229m"
COL_GREEN_MINT_121 = f"{ESC}[38;5;121m"
COL_GREEN_PALE_193 = f"{ESC}[38;5;193m"
COL_GREEN_LIME_154 = f"{ESC}[38;5;154m"
COL_GREEN_AQUA_85 = f"{ESC}[38;5;85m"
COL_GREEN_PALE_194 = f"{ESC}[38;5;194m"
COL_GREEN_DARKCYAN_23 = f"{ESC}[38;5;23m"
COL_CYAN_PURE_50 = f"{ESC}[38;5;50m"
COL_CYAN_PALE_195 = f"{ESC}[38;5;195m"
COL_CYAN_AQUAMARING_87 = f"{ESC}[38;5;87m"
COL_CYAN_GRAYISH_109 = f"{ESC}[38;5;109m"
COL_CYAN_LIGHT_51 = f"{ESC}[38;5;51m"
COL_CYAN_AQUA_14 = f"{ESC}[38;5;14m"
COL_BLUE_SKYBLUE_45 = f"{ESC}[38;5;45m"
COL_BLUE_MEDIUM_20 = f"{ESC}[38;5;20m"
COL_BLUE_DEEPSKY_39 = f"{ESC}[38;5;39m"
COL_BLUE_PALE_153 = f"{ESC}[38;5;153m"
COL_BLUE_LIGHTCOBALT_110 = f"{ESC}[38;5;110m"
COL_PURPLE_MAGENTA_164 = f"{ESC}[38;5;164m"
COL_PURPLE_MAGENTALIGHT_170 = f"{ESC}[38;5;170m"
COL_PURPLE_LAVENDER_141 = f"{ESC}[38;5;141m"
COL_PURPLE_PALEVIOLET_183 = f"{ESC}[38;5;183m"
COL_PINK_BRIGHT_198 = f"{ESC}[38;5;198m"
COL_PINK_LILAC_177 = f"{ESC}[38;5;177m"
COL_PINK_CANDY_218 = f"{ESC}[38;5;218m"
COL_WHITE_CREAM_230 = f"{ESC}[38;5;230m"
COL_WHITE_LIGHT_15 = f"{ESC}[38;5;15m"
COL_BROWN_94 = f"{ESC}[38;5;94m"
COL_BROWN_KHAKI_222 = f"{ESC}[38;5;222m"
COL_BROWN_COPPER_173 = f"{ESC}[38;5;173m"
COL_GRAY_246 = f"{ESC}[38;5;246m"
C_0 = f"{ESC}[0m"
C_GRY = f"{ESC}[90m"
C_RED = f"{ESC}[91m"
C_GRN = f"{ESC}[92m"
C_YLL = f"{ESC}[93m"
C_BLU = f"{ESC}[94m"
C_MAG = f"{ESC}[95m"
C_CYN = f"{ESC}[96m"
C_WHT = f"{ESC}[97m"
C_B = f"{COL_ORANGE_LIGHT_215}"
C_P = f"{COL_GREEN_AQUA_85}"
C_V = f"{COL_BLUE_DARK}"
C_SC0 = f"{COL_PURPLE_LIGHT}"
C_SC1 = f"{COL_PURPLE_MAGENTA_164}"
C_O = f"{COL_BLUE_LIGHT}"
C_0 = f"{COL_CYAN_PALE_195}"
C_1 = f"{COL_BLUE_PALE_153}"
# Color Title
C_T = f"{COL_BLUE_SKY}"
# Color Search
C_S = f"{COL_CYAN_PURE_50}"
C_SH = f"{COL_RED_STRAWBERRY_204}"
# Color File
C_F = f"{COL_ORANGE_214}"
# Color Highlight
C_H = f"{COL_WHITE_CREAM_230}"
# Color Information
C_I = f"{COL_CYAN_AQUA_14}"
# Color Code or Python
C_PY = f"{COL_GREEN_AQUA_85}"
# Color Question
C_Q = f"{COL_PINK_LILAC_177}"
# Console Output
C_PROG = f"{COL_PINK}"
# Color Warning
C_W = f"{C_YLL}"
# Color Error
C_E = f"{COL_RED}"
# COLOR Search Index
C_SI = f"{C_MAG}"
# COLOR Line Index
C_L = f"{C_PY}"
# Coloring A Date
C_D = f"{COL_BROWN_KHAKI_222}"
# Coloring A Search Match
C_M = f"{COL_RED_BRIGHT_196}"
# Coloring A Text Line
C_TX = f"{COL_WHITE_CREAM_230}"
# Coloring A Context Tag
C_C = f"{COL_GREEN_MINT_121}"
# Coloring A Bread Crumb
C_BR = f"{COL_CYAN_AQUA_14}"
# DIFF COLOR DELETED
C_DIFF_DEL = f"{COL_GRAY_246}{COL_STRIKETHROUGH}"
# DIFF COLOR ADDED
C_DIFF_ADD = f"{COL_ORANGE_214}"
# DIFF COLOR UNCHANGED
C_DIFF_UNCHANGED = f"{COL_CYAN_AQUA_14}"


# TODO Also generate these methods
def get_color_dict() -> dict:
    """returns the color constants as a dict"""
    color_dict = {
        k: f"{v}" for k, v in globals().items() if (k.isupper() and (k.startswith("C_") or k.startswith("COL_")))
    }
    return color_dict


# all colors in a color dict
COLOR_DICT = get_color_dict()


# get colored string
# TODO add a logic for background colors
def colorize(
    s: str,
    color: str,
    reset_col: Optional[str] = "COL_RESET",
    emoji: Optional[str] = None,
    strikethrough: bool = False,
    bold: bool = False,
    underline: bool = False,
) -> str:
    """colorize a string based on the string and also reset the color"""
    out = ""
    if not isinstance(s, str):
        return s
    col: str = COLOR_DICT.get(color, "")
    col_reset = "" if reset_col is None else COLOR_DICT.get(reset_col, "COL_RESET")

    if strikethrough:
        col += COL_STRIKETHROUGH
    if bold:
        col += COL_BOLD
    if underline:
        col += COL_UNDERLINE
    e_: str = emoji if emoji else ""
    # always reset background as the default reset sometimes doesn't seem to work
    col_reset_bg = COL_RESET_BG if len(col) > 0 else ""
    # now construct an output string and add reset sequence if needed
    # this also allows to have multiple formatting color codes like C_DIFF_DEL
    out = f"{e_}{col}{s}{col_reset_bg}{col_reset}"
    if not COL_RESET in out:
        # check if there are any additional formattings
        if len([f for f in [COL_STRIKETHROUGH, COL_BOLD, COL_UNDERLINE] if f in out]) > 0:
            out += COL_RESET
    return out


if __name__ == "__main__":
    # vars_dict = {k: f"{v}{k}{C_0}" for k, v in globals().items() if k.isupper()}
    for k, v in COLOR_DICT.items():
        print(colorize(k, k, reset_col="C_0"))
    # testing the additional formatting options
    print(colorize("STRIKTETHROUGH", color="C_PY", strikethrough=True, bold=False, underline=False))
    print(colorize("BOLD", color="C_PY", strikethrough=False, bold=True, underline=False))
    print(colorize("UNDERLINE", color="C_PY", strikethrough=False, bold=False, underline=True))
    print(colorize("ALL FORMATTINGS", color="C_PY", strikethrough=True, bold=True, underline=True, emoji="🤡"))
