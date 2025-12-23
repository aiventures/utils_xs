"""bat_helper: overcoming the quirks of batch files and breaking your fingers"""

import argparse
import os
from argparse import ArgumentParser
from typing import Tuple, Optional

from libs.helper import Persistence
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F, C_W


def _parse_env(args: dict) -> Tuple[Optional[str], Optional[str]]:
    """Parses ENV Variables from input string"""
    out = [None, None]

    params: str = args.get("params", "")
    params = params.strip()
    key_value = params.split(maxsplit=1)
    key = key_value[0]
    if len(key) == 0:
        print(f"🚨{C_E}bathelper: no params were passed{C_0}")
        return out

    value = None
    # if only one param is supplied pass that one
    if len(key_value) > 1:
        value = key_value[1]
    else:
        value = os.environ.get(key)

    return [key, value]


def save_env(args: dict) -> None:
    """Saves env variable"""
    p_output = args.get("p_output", "no_path")
    if not os.path.isdir(p_output):
        print(f"🚨{C_E}bathelper: Path [{p_output}] doesn't exist{C_0}")
        return

    key, value = _parse_env(args)
    if key is None:
        return

    if value is None:
        print(f"🚨{C_E}bathelper: Variable [{key}], no value was passed or is in environment{C_0}")
        return

    f_out = os.path.join(p_output, key)
    Persistence.save_txt(f_out, value)


def get_env(args: dict) -> Optional[str]:
    """reads the env from params.
    if p_input is given it will try to read a value from there
    if p_output is given it will also be saved to that location
    """
    p_input = "no_path" if args.get("p_input") is None else args.get("p_input")
    p_output = "no_path" if args.get("p_output") is None else args.get("p_output")
    p_input = p_input if os.path.isdir(p_input) else None
    p_output = p_output if os.path.isdir(p_output) else None
    key, value = _parse_env(args)
    if key is None:
        print(f"{C_W}bathelper: No environment param [{key}]{C_0}")
        return

    # no env value found, try to get from saved variable
    if value is None and p_input is not None:
        f_env = os.path.join(p_input, key)
        lines = Persistence.read_txt_file(f_env, comment_marker=None)
        if len(lines) > 0:
            value = lines[0].strip()
            # now set the environment value
            os.environ[key] = value
    if value is None:
        print(f"{C_W}bathelper: No value found for environment param [{key}]{C_0}")
        return

    # save to local path if given
    if p_output is not None:
        f_out = os.path.join(p_output, key)
        Persistence.save_txt(f_out, value)


def create_arg_parser() -> ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(description="Batch File Helper")
    parser.add_argument("--f_input", default=None, help="Input File")
    parser.add_argument("--p_input", default=None, help="Path Input")
    parser.add_argument("--f_output", default=None, help="Output File")
    parser.add_argument("--p_output", "--p-output", default=None, help="Path Output")
    parser.add_argument("--params", default=None, help="Passed Bat Params")

    parser.add_argument(
        "--action-save-env",
        "--action_save_env",
        action="store_true",
        help="Set an environment variable",
    )
    parser.add_argument(
        "--action-get-env",
        "--action_get_env",
        action="store_true",
        help="Get an environment variable",
    )

    return parser


def run_action(args: dict) -> None:
    """select and run action"""
    if args.get("action_save_env") is True:
        save_env(args)
    if args.get("action_get_env") is True:
        get_env(args)


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    args_dict = vars(args)
    run_action(args_dict)


if __name__ == "__main__":
    main()
