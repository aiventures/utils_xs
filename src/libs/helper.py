"""Some Python Helper functions"""

import os
import sys
import logging
import re

import argparse
import json
from json import JSONDecodeError

# import datetime
from datetime import timedelta, timezone
from datetime import datetime as DateTime
import shutil
import subprocess
import traceback
from pathlib import Path
from typing import Any, Dict, List, Union, Tuple, Optional
from zoneinfo import ZoneInfo
from configparser import ConfigParser
from dateutil import parser as date_parser
from bs4 import BeautifulSoup, Tag

# ANSI color codes
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F, C_W
from config.myenv import MY_CMD_EXIFTOOL, MY_P_PHOTO_DUMP, MY_P_PHOTOS_TRANSIENT

CMD_EXIFTOOL = MY_CMD_EXIFTOOL


logger = logging.getLogger(__name__)

# byte order mark for some utf8 file types
BOM = "\ufeff"


class Helper:
    """Some Helper Functions"""

    @staticmethod
    def show_progress(num_passed: int, total: int, text: str = None) -> None:
        """
        Display a progress bar on the terminal for file moving operations.

        The progress bar uses colored block emojis and shows percentage and count.

        Args:
            num_moved (int): Number of files moved so far.
            total (int): Total number of files to move.
        """
        if total == 0:
            return
        percent = num_passed / total if total else 1.0
        blocks_total = 20
        blocks_done = int(percent * blocks_total)
        blue_block = "🟦"
        green_block = "🟩"
        yellow_block = "🟨"
        orange_block = "🟧"
        red_block = "🟥"

        if percent < 0.5:
            progressbar = green_block * blocks_done + blue_block * (blocks_total - blocks_done)
        elif percent < 1.0:
            progressbar = (
                green_block * 10 + yellow_block * (blocks_done - 10) + blue_block * (blocks_total - blocks_done)
            )
        else:
            progressbar = green_block * 10 + yellow_block * 4 + orange_block * 4 + red_block * 2

        percent_display = int(percent * 100)
        output_text = text if text is not None else "Progress"
        sys.stdout.write(f"\r{C_T}{output_text}: {progressbar} {percent_display}% {C_I}({num_passed}/{total}){C_0}")
        sys.stdout.flush()
        if num_passed == total:
            print()

    @staticmethod
    def format_timestamp(timestamp: int, timezone_s: str = "Europe/Berlin", format_s: str = "%Y:%m:%d %H:%M:%S") -> str:
        """
        Convert a Unix timestamp to a formatted date string in a specified timezone.

        Parameters:
        - timestamp (int): The Unix timestamp to convert. Can be either:
            - 10 digits (seconds since epoch)
            - 13 digits (milliseconds since epoch)
        - timezone_str (str): IANA timezone name (e.g., "Europe/Berlin"). Defaults to "Europe/Berlin".
        - fmt (str): Format string for output, following Python's strftime directives.
            Defaults to "%Y:%m:%d %H:%M:%S".

        Returns:
        - str: The formatted date string in the specified timezone.

        Raises:
        - ValueError: If the timestamp is not 10 or 13 digits, or if the timezone is invalid.
        """

        ts_str = str(timestamp)
        if len(ts_str) == 13:
            timestamp /= 1000
        elif len(ts_str) != 10:
            raise ValueError("Timestamp must be either 10 or 13 digits long")

        # Convert to UTC datetime
        dt_utc = DateTime.fromtimestamp(timestamp, tz=timezone.utc)

        # Convert to target timezone
        try:
            dt_local = dt_utc.astimezone(ZoneInfo(timezone_s))
        except Exception as e:
            raise ValueError(f"Invalid timezone: {timezone_s}") from e

        # Format and return
        return dt_local.strftime(format_s)

    @staticmethod
    def format_seconds_offset(offset_s: int) -> str:
        """Format offset as (+/-)HH:MM.SS String"""
        sign = "+" if offset_s >= 0 else "-"
        abs_seconds = abs(offset_s)
        hours, remainder = divmod(abs_seconds, 3600)
        minutes, offset_s = divmod(remainder, 60)
        return f"{sign}{hours:02}:{minutes:02}:{offset_s:02}"

    @staticmethod
    def get_datetime_from_format_string(
        dt_str: str, time_format: str, timezone_s: str = "Europe/Berlin", offset: int = 0
    ) -> DateTime:
        """
        Created Using Prompt

        Convert a flexible datetime string into an ISO 8601 UTC datetime string.

        This function parses a datetime string using a user-defined format string,
        attaches a default timezone if none is provided, and converts the result
        to a UTC ISO 8601 string. It also detects and applies timezone suffixes
        such as 'Z', '+HH:MM', or '-HH:MM' if present at the end of the input.

        Supported format directives include:
        - %Y: Year
        - %m: Month
        - %d: Day
        - %H: Hour (24-hour)
        - %M: Minute
        - %S: Second
        - %f: Microsecond (use for milliseconds as well)

        Timezone suffixes must appear at the end of the string and follow ISO 8601:
        - 'Z' for UTC
        - '+HH:MM' or '-HH:MM' for offsets

        Args:
            dt_str (str): The datetime string to parse.
            time_format (str): The format string describing the structure of dt_str.
            default_timezone (str): IANA timezone name to apply if no suffix is present.

        Returns:
            Tuple[DateTime, Optional[str]]:
                - UTC DateTime (dt_utc.isoformat() ISO 8601
                  formatted UTC datetime string (e.g., '2024-08-01T12:38:32.499588Z')
                - Timezone suffix if detected ('Z', '+02:00', '-05:00'), otherwise None

        Raises:
            ValueError: If the datetime string cannot be parsed using the provided format.
        """
        # Detect timezone suffix
        tz_match = re.search(r"(Z|[+-]\d{2}:\d{2})$", dt_str)
        tz_info = tz_match.group(1) if tz_match else None
        dt_str_clean = dt_str[: -len(tz_info)] if tz_info else dt_str

        # Parse datetime
        try:
            dt_naive = DateTime.strptime(dt_str_clean, time_format)
        except ValueError as e:
            raise ValueError(f"Failed to parse datetime string: {e}")

        # Attach default timezone
        dt_local = dt_naive.replace(tzinfo=ZoneInfo(timezone_s))
        # apply offset
        if offset != 0:
            dt_local += timedelta(seconds=offset)

        # Apply timezone suffix if present
        if tz_info == "Z":
            dt_utc = dt_local.astimezone(timezone.utc)
        elif tz_info:
            offset_hours, offset_minutes = map(int, tz_info[1:].split(":"))
            offset_delta = timedelta(hours=offset_hours, minutes=offset_minutes)
            if tz_info.startswith("-"):
                offset_delta = -offset_delta
            tz = timezone(offset_delta)
            dt_local = dt_local.replace(tzinfo=tz)
            dt_utc = dt_local.astimezone(timezone.utc)
        else:
            dt_utc = dt_local.astimezone(timezone.utc)

        return dt_utc
        # return dt_utc.isoformat(), tz_info

    @staticmethod
    def get_utc_offset(
        dt_in: DateTime | str = None,
        timezone: str = "Europe/Berlin",
        time_format: str = "%Y:%m:%d %H:%M:%S",
        offset_sec: int = 0,
        as_string: bool = True,
    ) -> str | int:
        """
        Returns the UTC offset string for the given timezone, accounting for DST.

        Parameters:
        - tz_name: str — IANA timezone name (e.g., 'Europe/Berlin', 'America/New_York')
        - dt: DateTime — Optional DateTime object. Defaults to now.

        Returns:
        - str — Offset string in format ±HH:MM

        Example:
        - get_dst_offset_string("Europe/Berlin"))  # Might return "+02:00" during DST
        """

        # dt_str: str, time_format: str, default_timezone: str = "Europe/Berlin"

        dt = DateTime.now()
        if isinstance(dt_in, str):
            dt = Helper.get_datetime_from_format_string(dt_in, time_format, timezone)
        elif isinstance(dt_in, DateTime):
            dt = dt_in

        tz = ZoneInfo(timezone)
        localized_dt = dt.astimezone(tz)
        offset = localized_dt.utcoffset()

        # fallback
        if offset is None:
            offset = "+00:00" if as_string is True else 0
            return offset
        offset_out = int(offset.total_seconds())

        if as_string:
            offset_out = Helper.format_seconds_offset(offset_out)

        return offset_out


class CmdRunner:
    """Running Commands"""

    @staticmethod
    def run_cmd_and_stream(cmd: List[str], output_file: Path) -> bool:
        """
        Run exiftool with the given command and stream stderr to console.

        Args:
            cmd (List[str]): The exiftool command to execute.
            output_path (Path): Path to write stdout output (typically metadata.json).

        Returns:
            bool: True if the command succeeded, False otherwise.
        """
        out = []
        try:
            with output_file.open("w", encoding="utf-8") as outfile:
                process = subprocess.Popen(cmd, stdout=outfile, stderr=subprocess.PIPE, text=True)
                for line in process.stderr:
                    out.append(line.strip())
                    print(line.strip())
                process.wait()
            return process.returncode == 0
        except Exception as e:
            print(f"{C_E}Failed to run exiftool: {e}{C_0}")
            return False

    @staticmethod
    def run_cmd_and_print(cmd: List[str], decode: bool = True, show: bool = False, encoding: str = "latin1") -> list:
        """
        Run a command and print both stdout and stderr to the console in real time.


        Args:
            cmd (List[str]): The command to execute.

        Returns:
            bool: True if the command succeeded, False otherwise.
        """
        out = []
        try:
            # encoding: latin1 / cp1252 (windows) / utf-8
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding=encoding,
                # errors="replace",
            )

            # Stream both stdout and stderr
            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if stdout_line:
                    _s = stdout_line.strip()
                    if decode:
                        _s = _s.encode("latin1").decode("utf-8")
                    out.append(_s)
                    if show:
                        print(f"{C_PY}[CMD] {_s}{C_0}")
                if stderr_line:
                    _s = stderr_line.strip()
                    if decode:
                        _s = _s.encode("latin1").decode("utf-8")
                    out.append(_s)
                    if show:
                        print(f"{C_E}[ERR] {_s}{C_0}")

                if not stdout_line and not stderr_line and process.poll() is not None:
                    break
            return out

        except Exception as e:
            print(f"{C_E}Failed to run command: {e}{C_0}")

        return out


class Persistence:
    """persistence class"""

    @staticmethod
    def read_txt_file(filepath, encoding="utf-8", comment_marker="#", skip_blank_lines=True) -> list:
        """reads data as lines from file"""
        _filepath = Path(filepath)

        if not _filepath.is_file():
            print(f"{C_E} {_filepath} is not a valid file{C_0}")
            return []

        lines = []
        bom_check = False
        try:
            with open(str(_filepath), encoding=encoding, errors="backslashreplace") as fp:
                for line in fp:
                    if not bom_check:
                        bom_check = True
                        if line[0] == BOM:
                            line = line[1:]
                            logger.warning("Line contains BOM Flag, file is special UTF-8 format with BOM")
                    if len(line.strip()) == 0 and skip_blank_lines:
                        continue
                    if comment_marker is not None and line[0] == comment_marker:
                        continue
                    lines.append(line.strip())
        except:
            logger.error(f"Exception reading file {str(_filepath)}", exc_info=True)
        return lines

    @staticmethod
    def read_json(filepath: Path | str) -> Union[Dict[str, Any], List[Any]]:
        """
        Read a JSON file from a given filepath and return its content.

        Args:
            filepath (Path): Path to the JSON file to read.

        Returns:
            Union[Dict[str, Any], List[Any]]: Parsed JSON data as a dictionary or list.
        """
        _filepath = Path(filepath)
        try:
            with _filepath.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (TypeError, JSONDecodeError) as e:
            print(f"{C_E}Couldn't read [{_filepath}], {e}")
            return {}

    @staticmethod
    def save_txt(filepath: Path | str, lines: Optional[Union[str, List[str]]]) -> None:
        """
        Save a string or list of strings to a text file with exception handling.

        Args:
            filepath (Path): Path to save the file.
            lines (Union[str, List[str]]): Content to write. If string, converted to list.
        """
        if lines is None:
            # TODO add debug message
            return

        _filepath = filepath
        if isinstance(filepath, str):
            _filepath = Path(filepath)
        if isinstance(lines, str):
            out = lines
        else:
            out = "\n".join(lines)

        try:
            with _filepath.open("w", encoding="utf-8") as f:
                f.write(out)
            print(f"{C_H}Saved text file: {C_P}{_filepath}{C_0}")
        except Exception as e:
            print(f"{C_E}Failed to save file {_filepath}: {e}{C_0}")

    @staticmethod
    def save_json(filepath: Path | str, data: Optional[Dict[str, Any]]) -> None:
        """
        Save a dictionary to JSON, converting datetime objects to ISO strings.

        Args:
            filepath (Path): Path to save the JSON file.
            data (Dict[str, Any]): Data to save.
        """
        if data is None:
            # TODO Add DEBUG Message
            return

        _filepath = Path(filepath)

        def default_serializer(obj):
            if isinstance(obj, DateTime):
                return obj.isoformat()
            return str(obj)

        with _filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=default_serializer)

    @staticmethod
    def read_internet_shortcut(filepath: str) -> Optional[str]:
        """Reads an Internet shortcut (.url) and returns the URL if found."""
        cp = ConfigParser(interpolation=None)
        try:
            cp.read(filepath)
            return cp.get("InternetShortcut", "URL", fallback=None)
        except Exception:
            return None

    @staticmethod
    def collect_url_shortcuts(folder: Optional[Path] = None, filter_substring: Optional[str] = None) -> Dict[str, str]:
        """
        Reads all .url files in the given folder and returns a dictionary
        mapping filenames to their extracted URLs using read_internet_shortcut.
        Optionally filters URLs by a case-insensitive substring.

        Args:
            folder (Optional[Path]): Folder to scan. Defaults to current directory.
            filter_substring (Optional[str]): Substring to filter URLs (case-insensitive).

        Returns:
            Dict[str, str]: Dictionary with filename (str) as key and URL (str) as value.
        """
        folder = folder or Path.cwd()
        if not folder.exists() or not folder.is_dir():
            print(f"{C_E}Invalid folder: {folder}{C_0}")
            return {}

        url_dict = {}
        url_files = list(folder.glob("*.url"))
        print(f"{C_T}Found {len(url_files)} .url files in {C_P}{folder}{C_0}")

        for url_file in url_files:
            url = Persistence.read_internet_shortcut(str(url_file))
            if url:
                if filter_substring is None or filter_substring.lower() in url.lower():
                    url_dict[url_file.name] = url
                else:
                    print(f"{C_E}Filtered out: {url_file.name} (URL does not match filter){C_0}")
            else:
                print(f"{C_E}No URL found in {url_file.name}{C_0}")

        return url_dict


class Transformer:
    """Transforming stuff"""

    @staticmethod
    def md2toc(f: str, as_string: bool = True):
        """reads contents of a markdown file, extracts header lines to table of contents
        returns header lines as string or list
        """
        RE_SPECIAL_CHARS = "[\\\;:().,;/]"

        REGEX_HEADER = "^(#+) (.+)\n"
        REGEX_LINK = r"\[(.+)\]\(.+\)"
        MD_ANCHOR = "[_LABEL_](#_LINK_)"
        MD_INDENT = 2
        lines_toc = []
        lines_in = Persistence.read_txt_file(f, comment_marker="xxx")
        for l in lines_in:
            match = re.findall(REGEX_HEADER, l)
            if match:
                level = len(match[0][0])
                label = match[0][1].strip()
                link_text = re.findall(REGEX_LINK, label)
                if link_text:
                    label = link_text[0]

                # replace special characters
                link = re.sub(RE_SPECIAL_CHARS, "", label)
                link = link.replace(" ", "-").lower()
                anchor_link = MD_ANCHOR.replace("_LABEL_", label)
                anchor_link = anchor_link.replace("_LINK_", link)
                out_string = (level - 1) * MD_INDENT * " " + "* " + anchor_link + " " * MD_INDENT
                lines_toc.append(out_string)
        if as_string:
            return "\n".join(lines_toc) + "\n"
        else:
            return lines_toc

    @staticmethod
    def create_timestamp_from_time_string(
        time_str: Union[str, None], filename: str | None, folder: Path | None, timezone: str = "Europe/Berlin"
    ) -> Union[Dict[str, Any], None]:
        """
        Convert a hh:mm:ss time string into a timezone-aware datetime and UTC timestamp.

        Args:
            time_str (Union[str, None]): Time string in format hh:mm:ss (1–2 digits per part).
            folder (Path): Folder where json will be saved.
            timezone (str): Timezone name (default: Europe/Berlin).

        Returns:
            Dict[str, Any]: Dictionary with keys:
                - "original": original time string
                - "utc": UTC datetime string
                - "timestamp": UTC timestamp in milliseconds
                - "datetime": datetime.datetime object
        """

        if time_str is None:
            time_str = input(f"{C_Q}Enter time string (hh:mm:ss): {C_0}").strip()

        try:
            parts = [int(p) for p in time_str.split(":")]
            while len(parts) < 3:
                parts.append(0)  # pad missing seconds or minutes
            hour, minute, second = parts[:3]

            # Use today's date with provided time
            local_zone = ZoneInfo(timezone)
            today = DateTime.date.today()
            dt_local = DateTime(today.year, today.month, today.day, hour, minute, second, tzinfo=local_zone)
            dt_utc = dt_local.astimezone(DateTime.timezone.utc)
            utc_str = dt_utc.isoformat()
            timestamp_ms = int(dt_utc.timestamp() * 1000)

            result = {"original": time_str, "utc": utc_str, "timestamp": timestamp_ms, "datetime": dt_utc}
            if filename:
                Persistence.save_json(folder / filename, result)
                print(f"{C_H}Saved timestamp to {C_P}{folder / filename}{C_0}")
            return result

        except Exception as e:
            print(f"{C_E}Failed to parse time string: {e}{C_0}")
            return None


if __name__ == "__main__":
    loglevel = logging.INFO
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(module)s:[%(name)s.%(funcName)s(%(lineno)d)]: %(message)s",
        level=loglevel,
        stream=sys.stdout,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    t = "2025:11:30 12:00:00"
    # UTC + OFFSET
    offset = Helper.get_utc_offset(t)
    print(offset)
