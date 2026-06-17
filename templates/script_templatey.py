"""script_template.py boilerplate code to write a script including arfparse arguments"""

from __future__ import annotations
import argparse
import copy
import datetime
import json
import os
import sys
import re
import traceback
import logging
from os import listdir
from copy import deepcopy
from datetime import datetime as DateTime
from datetime import timezone

# import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Literal
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, Tag

# from configparser import ConfigParser
from dateutil import parser as date_parser
from config.color_logger import setup_color_logging

# ANSI color codes
from config.colors import (
    C_0,
    C_B,
    C_E,
    C_F,
    C_H,
    C_I,
    C_L,
    C_P,
    C_PY,
    C_Q,
    C_S,
    C_T,
    C_W,
)

# get read/write path from env / create the json using bat2py.bat
from config.constants import ENV_DICT

# TODO 🟡 create a waypoint file from jpg files / right now this is a bat file

# custom print commands / note that MY_ENV_PRINT_SHOW_EMOJI and MY_ENV_PRINT_SHOW_EMOJI
# need to be set accordingly in environment to reflect certain debug levels
from libs.custom_print import (
    print_json,
    printd,
    printe,
    printw,
    printt,
    printh,
    printi,
    set_print_level,
    printpy,
    inputc,
)

RUN_ACTION_TEST: str = "action_test"

# ensure root logger will use colored logger
setup_color_logging(use_color=True, use_emoji=True, indent=120)
logger = logging.getLogger(__name__)


class MarkDownParser:
    """Parsing Markdown Documents"""

    def __init__(self, action_test: bool = False, f_markdown: Optional[str] = None):
        """Constructor."""
        self._actions: dict[bool] = {}
        if f_markdown is None:
            logger.error("Markdown Filepath  --f_markdown is empty ")
            return

        self._actions = {RUN_ACTION_TEST: action_test}
        self._f_markdown: Path = Path(f_markdown).absolute()

    @classmethod
    def create_markdown_parser(cls, args: argparse.Namespace) -> Optional[MarkDownParser]:
        """create an image Organizer instance"""
        logger.debug("start")
        arg_dict = vars(args)

        return cls(
            action_test=arg_dict.get("action_test"),
            f_markdown=arg_dict.get("f_markdown"),
        )

    def run(self) -> None:
        """runs all actions. will be defined by actions dict"""
        logger.debug(f"Start actions {self._actions}")
        for func, run in self._actions.items():
            if run:
                logger.debug(f"Running Action [{func}()]")
                getattr(self, func)()

    def action_test(self) -> None:
        """Runs the test actions, will be called programmatically"""
        logger.debug("start")
        pass

    @staticmethod
    def argparse_set_defaults(args: argparse.Namespace) -> argparse.Namespace:
        """Sets the argparse defaults if not already covered by defaults"""
        logger.debug("start")

        # modify default values ....

        return args

    @staticmethod
    def build_arg_parser() -> argparse.ArgumentParser:
        """
        Command Line Interface to MarkdownParser
        Returns:
            argparse.ArgumentParser: Configured argument parser.
        """
        parser = argparse.ArgumentParser(description="Markdown Parser Utility")

        # used in main / OK
        parser.add_argument(
            "--action_test",
            "--action-test",
            action="store_true",
            help="Do Some Tests (temporary)",
        )

        parser.add_argument(
            "--f_markdown",
            "--f-markdown",
            "-f",
            type=str,
            default=None,
            help="Filename Of Markdown Document",
        )

        parser.add_argument(
            "--action_show_args",
            "--action-show-args",
            action="store_true",
            help="Show the arparse args when running the image organizer",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--print_level",
            "--print-level",
            type=str,
            default="INFO",
            help="Print Level (DEBUG,INFO,WARNING,ERROR), if not set as ENV MY_PRINT_LEVEL (Default: INFO)",
        )
        return parser


def main(args_overwrite: Optional[list[str]] = None) -> None:
    """Run the Markdown Parser"""

    # parse from commmand line
    parser = MarkDownParser.build_arg_parser()

    # overwrite arguments / https://stackoverflow.com/questions/54050343/how-to-set-variables-value-in-command-line-using-argparse-or-sys-avrg
    # myprog --foo 10 --bar x y z => parser.parse_args(["--flag", "value", "pos1", "pos2"])
    args = None
    if args_overwrite is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args_overwrite)
    # set defaults
    args = MarkDownParser.argparse_set_defaults(args)

    # set print level / default is info
    if os.environ.get("MY_PRINT_LEVEL") is None:
        set_print_level(args.print_level, show_emoji=True)

    if args.action_show_args:
        print_json(vars(args), "ARGPARSER SETTINGS")

    # Run the Actions
    markdown_parser = MarkDownParser.create_markdown_parser(args)
    markdown_parser.run()


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    if True:
        # testing the module
        args = ["--action_show_args", "--action_test", "--print_level", "DEBUG"]
        main(args)
    else:
        main()
