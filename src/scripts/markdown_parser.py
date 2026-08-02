"""markdown_parser.py parsing and searching markdown"""

from __future__ import annotations
import argparse
from argparse import ArgumentParser, Namespace
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
from libs.environment import Environment, MY_ENV_PRINT_LEVEL, F_MARKDOWN_TEST, MY_P_MYENV
from libs.helper import Persistence, Helper

# ANSI color codes
# from config.colors import colorize
# custom print commands / note that MY_ENV_PRINT_SHOW_EMOJI and MY_ENV_PRINT_SHOW_EMOJI
# need to be set accordingly in environment to reflect certain debug levels
from libs.custom_print import (
    print_json,
    print_infoline,
    set_print_level,
)

# get read/write path from env / create the json using bat2py.bat
from config.constants import ENV_DICT

# TODO 🟡 create a waypoint file from jpg files / right now this is a bat file
# TODO 🟡 Allow to search via regex and matching
# TODO 🟡 Add Batch Scripts
# TODO 🟡 Allow to add tags / emojis in lines
# TODO 🟡 Aloow to open file explorer / export commands to a temproary file
# TODO 🟡 Extract paths
# TODO 🟡 Resolve relative path

RUN_ACTION_TEST: str = "action_test"

# ensure root logger will use colored logger
setup_color_logging(use_color=True, use_emoji=True, indent=120)
logger = logging.getLogger(__name__)

# Place a .env file with F_MARKDOWN_TEST containing the path to a sample markdown document
# By Default the environment si set in /utils_xs/.env
environment = Environment()


class MarkDownParser:
    """Parsing Markdown Documents"""

    def __init__(
        self,
        f_markdown: Optional[str] = None,
        p_env: Optional[str | Path] = None,
        f_cmd_open_path: Optional[str] = "markdownparser_open_path.bat",
    ):
        """Constructor."""
        logger.debug(f"start, markdown [{f_markdown}], temporary path []")
        if f_markdown is None:
            logger.error("Markdown Filepath no filepath was referenced")
            return

        self._f_markdown: Path = Path(f_markdown).absolute()
        # get the parent path of the file so as to calculate a relative path
        self._p_parent = self._f_markdown.parent
        # path to store temporary command file
        self._p_env: Optional[Path] = Path(p_env).absolute() if p_env and Path(p_env).is_dir() else None
        # create apath to a script that will be generated to allow to be opened in Windows File explorer
        self._f_cmd_open_path: Optional[Path] = None
        if self._p_env and f_cmd_open_path:
            self._f_cmd_open_path = self._p_env.joinpath(f_cmd_open_path)

        self._lines: dict = {}
        self._index: dict = {}
        self._info_lines: dict = {}
        # read the markdown and create the title index
        self._read_markdown()
        self._create_info_lines()
        # get links from each line

    def _read_markdown(self) -> None:
        """reads the markdown file"""
        _lines = Persistence.read_txt_file(self._f_markdown, comment_marker=None, skip_blank_lines=False)
        logger.debug(f"Read [{len(_lines)}] lines from file [{str(self._f_markdown)}]")
        self._lines = {index: value for index, value in enumerate(_lines, start=1)}

    def _create_info_lines(self) -> None:
        """reads the markdown and creates a toc index for each line (hierarchy)
        Given a list of markdown lines, return a dictionary:
        line_number -> list of active header hierarchy at that line.
        """
        header_stack = []  # e.g. ["h1", "h1.1", "h1.1.1"]
        result = {}
        header_regex = re.compile(r"^(#{1,6})\s+(.*)$")
        num_content: int = 0
        num_links: int = 0
        num_markdown: int = 0
        num_paths: int = 0

        for idx, line in self._lines.items():
            match = header_regex.match(line)
            if match:
                hashes, title = match.groups()
                level = len(hashes)

                # Ensure stack is correct length
                if len(header_stack) < level:
                    # Extend stack
                    header_stack.extend([None] * (level - len(header_stack)))
                else:
                    # Trim deeper levels
                    header_stack = header_stack[:level]

                header_stack[level - 1] = title.strip()

            # Store a *copy* of the current hierarchy for this line
            result[idx] = header_stack.copy()
            # merge everything into one dict
            # only line as content if it starts with a * or a -
            line_ = self._lines[idx].strip()
            content_line = None
            if len(line_) > 0 and line_[0] in ["*", "-"]:
                num_content += 1
                content_line = num_content

            # extract the links and markdowns
            markdown_links_: list = []
            links_: list = []
            link_map_: dict = {}
            path_map_: dict = {}

            if len(line_) > 0:
                links_ = MarkDownParser.extract_links(line_)
                # get old and new links in a map
                link_map_ = Helper.extract_hyperlinks(line_)
                markdown_links_ = MarkDownParser.extract_markdown_links(line_)
                num_links += len(links_)
                num_markdown += len(markdown_links_)
                # TODO Add Only Valid Paths
                path_map_ = Helper.extract_paths(line_, self._p_parent, is_path=False, is_file=False)

            self._info_lines[idx] = {
                "line": idx,
                "text": self._lines[idx],
                "hierarchy": result[idx],
                "breadcrumb": " > ".join(result[idx]),
                "markdown_links": markdown_links_,
                "links": links_,
                "link_map": link_map_,
                "path_map": path_map_,
                "content": content_line,
            }

            # if len(path_map_) > 0:
            #     logger.debug(json.dumps(self._info_lines[idx], indent=4, default=str))

        logger.debug(f"Found [{num_links}] links, [{num_markdown}] markdown links")

        self._index = result

    def _extract_links(self) -> None:
        """extract links from each line"""
        pass

    def _get_markdown_dict(self) -> dict:
        """transforms the data into an output dict"""
        out = {}
        return out

    def show(self):
        """shows the markdown as a formatted document"""
        # todo turn index into breadcrumbs
        # print(json.dumps(self._info_lines, indent=4, default=str, ensure_ascii=False))
        for _, line_info in self._info_lines.items():
            if not line_info["content"]:
                continue
            line = line_info["line"]
            text_ = line_info["text"]
            breadcrumb_ = line_info["breadcrumb"]
            hierarchy_ = line_info["hierarchy"]
            date_: Optional[str] = None
            if len(hierarchy_) > 0:
                # try to parse the breadbrumb hierarchy as datetime string YYYY-MM-DD
                try:
                    dt_ = Helper.get_datetime_from_format_string(hierarchy_[-1], time_format="%Y-%m-%d")
                    date_ = f"{hierarchy_[-1]}/{Helper.weekday_abbrev(dt_, language='de')}"
                except ValueError:
                    pass

            print_infoline(
                text=text_,
                # index=43,
                line_number=line,
                num_digits=3,
                date=date_,
                # contexts=["@context1"],
                # search_matches=["ist"],
                breadcrumb=breadcrumb_,
                text_length=80,
                show=True,
            )

        # print(self._index)
        # print(self._lines)
        pass

    @staticmethod
    def extract_markdown_links(line: str) -> list:
        """Extract Markdown PAttern."""
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        return re.findall(pattern, line)

    @staticmethod
    def extract_links(line: str) -> list:
        """extreact hyperlinks from both plain urls and markdown"""
        link_dict: dict = Helper.extract_hyperlinks(line)
        links: list = []
        for _, link_info in link_dict.items():
            links.append(link_info["new"])

        # get markdown links / and avoid duplicates that's why we also transfomr any links
        links_md: list = [l[1] for l in MarkDownParser.extract_markdown_links(line)]

        # clean up wrong links (additional closing parentheses from markdown links)
        out: list = []
        for link in links:
            if len([link_md for link_md in links_md if f"{link_md})" == link]) > 0:
                continue
            out.append(link)
        links = out
        links_md.extend(links)
        links = [l for l in links_md if l.lower().startswith("http")]
        return list(set(links))


class MarkdownArgParser:
    """command line input class wrapping the MarkdownParser class"""

    def __init__(self, default_arg_values: Optional[dict] = None):
        self._arg_parser: ArgumentParser = self.create_arg_parser()
        self._args: dict[str, str] = {}
        self._default_arg_values: dict = {} if default_arg_values is None else default_arg_values
        self._markdown_parser: Optional[MarkDownParser] = None
        logger.debug(f"Parser Constructor, default values: {self._default_arg_values}")

    def show_args(self) -> bool:
        """getter for  action_show_args"""
        if self._args.get("action_show_args", False):
            print_json(self._args, "ARGPARSER SETTINGS")

    def run(self) -> None:
        """Runs all actions."""
        ignore_actions = ["action_show_args"]
        # process all flags starting with an action prefix
        for method, value in self._args.items():
            if not method.startswith("action_") or method in ignore_actions:
                continue
            # run the method if it exists
            if callable(getattr(self, method, None)) and value is True:
                logger.debug(f"Running action [{method}], calling the method")
                getattr(self, method)()

    @property
    def f_markdown(self) -> Optional[Path]:
        """returns the absolute file path to the markdown file"""
        f_markdown_ = Path(self._args.get("f_markdown", "invvalid_path")).absolute()
        return f_markdown_ if f_markdown_.is_file() else None

    @property
    def p_env(self) -> Optional[Path]:
        """returns the path to temporsry command files"""
        p_env_ = Path(self._args.get("p_env", "invvalid_path")).absolute()
        return p_env_ if p_env_.is_dir() else None

    def action_test(self):
        """testing only"""
        logger.debug("start")
        self._markdown_parser.show()

    def create_arg_parser(self) -> ArgumentParser:
        """
        Command Line Interface to MarkdownParser
        Returns:
            argparse.ArgumentParser: Configured argument parser.
        """
        logger.debug("begin")
        parser = ArgumentParser(description="Markdown Parser Utility")

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
            "--p_env",
            "--p-env",
            type=str,
            default=None,
            help="Path to temporary command file snippets",
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

    def _set_defaults(self) -> None:
        """Setting default values in case not supplied already"""
        for key, default_value in self._default_arg_values.items():
            if self._args.get(key) is not None:
                continue
            self._args[key] = default_value

    # overwrite arguments / https://stackoverflow.com/questions/54050343/how-to-set-variables-value-in-command-line-using-argparse-or-sys-avrg
    # myprog --foo 10 --bar x y z => parser.parse_args(["--flag", "value", "pos1", "pos2"])
    def parse_args(self, args_list: Optional[list] = None) -> dict:
        """parses args and returns args"""
        if args_list is None:
            self._args = vars(self._arg_parser.parse_args())
        else:
            self._args = vars(self._arg_parser.parse_args(args_list))
        # also set some default values
        self._set_defaults()
        self._markdown_parser = MarkDownParser(self.f_markdown, self.p_env)
        return self._args


def main(args_overwrite: Optional[list[str]] = None, default_arg_values: Optional[dict] = None) -> None:
    """Run the Markdown Parser"""

    # parse from commmand line
    arg_parser = MarkdownArgParser(default_arg_values)
    _ = arg_parser.parse_args(args_overwrite)

    # set print level / default is info
    set_print_level(environment.get(MY_ENV_PRINT_LEVEL, "DEBUG"), show_emoji=True)
    arg_parser.show_args()
    arg_parser.run()

    # # Run the Actions
    # markdown_parser = MarkDownParser.create_markdown_parser(args)
    # markdown_parser.run()


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    # get the path to a test markdown file
    f_markdown_test = environment.get(F_MARKDOWN_TEST, None, check="file")
    # get the path to the temporay files
    p_myenv = environment.get(MY_P_MYENV, None, check="path")

    # get the path to a temporary directiry (so as to store temporary commands for
    # later run shell / command line )

    # just for testing import a path pointing to a local markdown file
    if True:
        # f_markdown_test = environment.get(F_MARKDOWN_TEST, None, check="file")
        if not f_markdown_test:
            sys.exit(0)
        # testing the module
        args = ["-f", f_markdown_test, "--action_show_args", "--action_test", "--print_level", "DEBUG"]
        if p_myenv:
            args.extend(["--p_env", p_myenv])
        main(args)
    else:
        main()
