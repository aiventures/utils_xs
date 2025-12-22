"""bat_helper: overcoming the quirks of batch files and breaking your fingers"""

import argparse
import os
from argparse import ArgumentParser

from libs.helper import Persistence
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F, C_W


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


def save_env(args: dict) -> None:
    """Saves env variable"""
    p_output = args.get("p_output", "no_path")
    if not os.path.isdir(p_output):
        print(f"🚨{C_E}Path [{p_output}] doesn't exist{C_0}")
        return
    params: str = args.get("params", "")
    params = params.strip()
    key_value = params.split(maxsplit=1)
    key = key_value[0]
    value = None
    # if only one param is supplied pass that one
    if len(key_value) > 1:
        value = key_value[1]
    else:
        value = os.environ.get(key)
    if value is None:
        print(f"🚨{C_E}Variable [{key}], no value was passed or is in environment{C_0}")
        return
    f_out = os.path.join(p_output, key)
    Persistence.save_txt(f_out, value)


def run_action(args: dict) -> None:
    """select and run action"""
    if args.get("action_save_env") is True:
        save_env(args)


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    args_dict = vars(args)
    run_action(args_dict)


if __name__ == "__main__":
    main()
