#!/usr/bin/env python3
"""Moves Image according to their timestamps.

SUMMARY

This Python program automates organizing image files by their creation dates extracted from metadata.
It uses exiftool to recursively scan a specified input folder for images with defined suffixes,
generating a JSON metadata file. The metadata is processed to map each image’s unique identifier
(last four digits of its filename) to its creation date. The program then creates date-based folders
(YYYYMMDD) in a specified output root and moves each image into the appropriate dated folder, displaying
a colorful progress bar during the move. It supports command-line arguments or interactive input for
input/output paths, handles errors for unmapped files, and employs ANSI colors for enhanced console messaging.
The implementation is modular with clear docstrings and type hints for maintainability and reuse.

PROMPT

V4 - Save Time Offset
add a function to calculate the time offset T_CAMERA - T_GPS = T_OFFSET. It also receives a
timezone with a default of Europe/Berlin - assume the current path as directory - read the json
files TIMESTAMP_GPS and TIMESTAMP_CAMERA. Display the original timestamps and calculate the time_offset
in seconds from "timestamp" field. - In case the TIMESTAMP_GPS file is missing, ask the user for input
of the datetime in the form hh:mm:ss. Recalculate this string as timestamp for the given timezone and
calculate the utc 13 digits timestamp and calculate the time_offset - if file TIMESTAMP_CAMERA or both
TIMESTAMP_CAMERA and TIMESTAMP_GPS are missing, issue an error message and set the offset to 0. - Finally,
save the offset in seconds into a file offset.env in the same path. - Modularize the save function into
a save_txt function receiving file path and a parameter lines being either a list of strings or a string.
If a string, convert it to a one element list. save the list using "\n".join(list...) into the text file

V3 - Input the time from GPS
write a function receiving a time string to be expected as a colon separated string of time hh:mm:ss (each
part can be a one or two digit number). another parameter is timezone with a default timezone of "Europe/Berlin".
if the time string is not passed (None), then ask the user for an input of the time string.
Calculate the corresponding datetime in the same output structure as extract_image_timestamp (without the filename attribute).
Also save this dict as gps_timestamp.json to the folder.

V2 - Get the timestamp of an image to be used as offset parameter
add another function that extracts a timestamp in an image from exifdata using exiftool. In commandline
the command is exiftool -SubSecDateTimeOriginal -b gps.jpg Output look like:
"2025:08:31 16:34:46.22+02:00" Write a function that will use a filepath as input for the image file.
If filepath is empty, check for fallback - In current path, check for a gps.jpg file. if present,
use this - If not available, show all *.jpg files in the out output, and assign them a number
(loop over all jpg file and use enumerate) in the output, for each file like [number] filename.jpg.
Ask the user for the number and us the assigned image file to be used - return the retrieved timestamp
in a dictionary with the following attrbutes - "original": the original timestamp string as extracted
by exiftool - "utc": the time stamp string but converted to utc time (string has offset +00:00)
- "timestamp" the timestamp in UTC time in miliseconds (13 digits) - "datetime": the
corresponding datetime.datetime object for the datetime string - add a dedicated save_json
function to store the json file receiving filename and data as dict. Also adjust datetime
attribute fields to be able to be stored as json (not leading to errors) -
save this dict as gps_offset.json in the path where the file is located

V1 - update metadata.json for output folders
add another function:  check the --output folder and all its first level children folders and apply
the run_exiftool on each of those folders to update the metadata.json files there
add another argparse argument -u --update to run this function from command line

ORIGINAL

Program Overview
- write a program using Python to automatically create folders by date and move image files from a path where image files were dumped
- As Input Image, use image files with that are defined for a set of image suffixes: image_suffixes=["jpg","jpeg","heif","png","tif"] .
  The file name usually conforms to a length of 8 Characters with the last 4 characters being a numerical character, in short an image
  file looks like ccccnnnn.jpg (c any character, n a number 0123456789).
steps to do this
- Use a F_CMD_EXIF variable to define the location of the exiftool.exe file
- Use a default path P_IMAGE_DUMP_DEFAULT as a default source root folder and P_OUTPUT_ROOT_DEFAULT as a default root folder
- Add argparse arguments for P_IMAGE_DUMP (default P_IMAGE_DUMP_DEFAULT) and root folder P_OUTPUT_ROOT (default P_OUTPUT_ROOT_DEFAULT) for output folders.
- For the case nothing is supplied, ask the user for the path. In case user will enter nothing for the output root folder path, then use P_OUTPUT_ROOT_DFEFAULT.
  If nothing is entered for the input folder, use the current folder as input folder.

Program steps
- In path P_IMAGE_DUMP_DEFAULT, execute the command F_CMD_EXIF -r -g -ext jpg -ext jpeg -json . > P_OUTPUT_ROOT/metadata.json
  - For F_CMD_EXIF, use the path to the exiftool executable
  - Export rhe metadata.json to the folder stored in P_OUTPUT_ROOT
  - For the set of -ext parameters use the suffixes defined in the image_suffixes list
  - the P_OUTPUT_ROOT/metadata.json file will be a json list of entries (one entry per image file).
    ```
        [
        {"SourceFile": "./ccccnnnn.JPG",
         "Composite":{
           "SubSecDateTimeOriginal": "2025:06:07 16:10:27.065+02:00",
         }
        }
        ]
        ```
  - Sections for each entry that need to be analyzed is
    "SourceFile" containing the file name ccccnnnn.JPG" and "Composite['SubSecDateTimeOriginal']" containing a datetime string with timezone:
        "2025:06:07 16:10:27.065+02:00" (%Y:%m:%d %H:%M:%S.%f+%z) with
        %Y — 4-digit year (YYYY)
        %m — 2-digit month (MM)
        %d — 2-digit day (DD)
        %H — 2-digit hour (24-hour)
        %M — 2-digit minute
        %S — 2-digit second
        %z — time zone offset (+/-hhmm)
        %f — fractional seconds
  - Perform the following tasks:
    - read the P_OUTPUT_ROOT/metadata.json (using a read_json function) into a dict file_dict
        - process all image entries and create an output dictionary file_dict:
          - as key use the "nnnn" part of the file
          - as value for each dict entry use the following attributes
            - "key": the "nnnn" part of each file from "SourceFile"
                - "filename": field contents of  "SourceFile", but without the path
        - "datetime_created": datetime.dateime object transformed from SubSecDateTimeOriginal (using correct time zone offset)
                - "date": datetime_created transformed as an 8 character string matching YYYYMMDD
        - save this output dictionary to the selected input folder named file_dump.json. Also take care to transform datetime_created
          into a string before saving to json (otherwise you'd get an error).
        - also collect all occured dates (YYYYMMDD) in a date_list. make sure date_list doesn't contain duplicates.
        - move all files in the P_IMAGE_DUMP_DEFAULT to another path according to the output dictionary and the date_list:
          - Create new path folders below P_OUTPUT_ROOT: Loop through all date strings in the date_list list. If not already created,
            create a new folder according to the date schema YYYYMMDD as child paths in P_OUTPUT_ROOT
          - Now Loop over all file names in P_IMAGE_DUMP and move each file according to this logic:
            - From the file name of each file in the path,  extract any occuring sequence consisting of numbers only. If found,
                  truncate this number to the last four digits.
                - use these last four digits as key to look up in the file_dict dictionary. If found move that file to the correspinding
                  folder in P_OUTPUT_ROOT/YYYYMMDD, with YYYYMMDD the value found in "date" attribute of the dict entry
    - during file move show a progress bar (perecentage of files moved, with the number of files in the input folder) using
          output of the progress in a single line using things like:
          ```
                sys.stdout.write(f"\rProgress: {i}%")
                sys.stdout.flush()
          ```
          The progress bar should always have a length of 20 characters, and block emojis of different colors represent 5% progress each
          🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 should represent 0% progress (blue is not completed )
          🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 should represent 50%
          🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟨🟨🟨🟨🟧🟧🟧🟧🟥🟥 should represent 100%
    - Also add a string (n/N) Files moved behind the progress bar (n number of files moved, N total number of files)
        - collect any file names where no dict entry could be found.
        - after moving is completed, list all files that couldn't be moved as error messages. Or in case all file could be moved, isssue a success message

Also add to the program
- Add ANSI COLOR CODES so it is possible to use colored output using f strings like f"{C_T}text{C_0}".
  Use following Color Codes according to their denoted meaning and proposals for ansi color code to use
  rem reset all color formatting
  - C_0 (COL_RESET) is used for resetting color to default pronpt colors
  - C_T (COL_BLUE_SKY)
  - C_S search keys (COL_ORANGE)
  - C_F file keys for rendering file paths (COL_BLUE_SKY)
  - C_H highlighted output of print text (COL_YELLOW_PALE_229)
  - C_PY program output like print statements from python (COL_GREEN)
  - C_Q prompt color for user input
  - C_PROG When the program name is used as output this color code is used (COL_PINK)
  - C_ERR and C_E Error message color
  - C_I Index number color  in a list (COL_GREEN_AQUA_85)
- Add color codes to the output / print statements
- modularize logic into functions for future reuse
- use a main function and put the logic into a def main function so that the program can also run stand alone
- for constructing paths and to ensure cross platform compatibility, use Path from pathlib module
- add docstrings to each function
- add type hints to all functions and variable declarations. Add new typing definitions such as Union
- move the argparser construction into a separate function

"""

import re
import argparse
import json
from json import JSONDecodeError
import datetime
import shutil
import subprocess
import traceback
import sys
from pathlib import Path
from typing import Any, Dict, List, Union
from dateutil import parser as date_parser
from zoneinfo import ZoneInfo
from configparser import ConfigParser

# ANSI color codes
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B
from config.myenv import MY_CMD_EXIFTOOL, MY_P_PHOTO_DUMP, MY_P_PHOTOS_TRANSIENT

# Paths from environemt
# Define image suffixes and default paths
IMAGE_SUFFIXES = ["jpg", "jpeg", "raf", "dng"]
CMD_EXIF = MY_CMD_EXIFTOOL
P_PHOTO_DUMP_DEFAULT = Path(MY_P_PHOTO_DUMP)
P_PHOTOS_TRANSIENT_DEFAULT = Path(MY_P_PHOTOS_TRANSIENT)

# Timestamp files to calculate offset
# T_CAMERA - T_GPS = T_OFFSET
F_TIMESTAMP_GPS = "timestamp_gps.json"
F_TIMESTAMP_CAMERA = "timestamp_camera.json"
F_OFFSET = "offset.env"


def read_internet_shortcut(f: str, showinfo=False):
    """reads an Internet shortcut from filepath, returns the url or None
    if nothing could be found"""
    url = None
    cp = ConfigParser(interpolation=None)

    try:
        cp.read(str(f))
    except Exception as ex:
        print(f"--- EXCEPTION read_internet_shortcut:{ex} ---")
        print(traceback.format_exc())
        return None

    sections = cp.sections()

    for section in sections:
        options = cp.options(section)
        if showinfo:
            print("Section:", section)
            print("- Options:", options)

        for option in options:
            v = cp.get(section, option)
            if showinfo:
                print(f" {option} : {v}")
            if (section == "InternetShortcut") and (option == "url"):
                url = v

    return url


def create_openstreetmap_shortcut(lat: float, lon: float) -> str:
    """Shorcut Link"""
    shortcut_lines = ["[InternetShortcut]", f"URL=https://www.openstreetmap.org/#map={lat:.7f}/{lon:.5f}"]
    shortcut = "\n".join(shortcut_lines)
    return shortcut


def get_base_exiftool_cmd(input_folder: Path) -> list:
    """creates the base exiftool command to export image data"""
    suffix_args = []
    for ext in IMAGE_SUFFIXES:
        suffix_args.extend(["-ext", ext])

    # command to export all exifdata in groups as json for given suffixes
    # progress is shown every 50 images
    # the c command is to format gps coordinates as decimals
    exif_cmd = [CMD_EXIF, "-r", "-g", "-c", "'%.6f'", "-progress50"] + suffix_args + ["-json", str(input_folder)]
    return exif_cmd


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Create and return a command-line argument parser for the program.

    The parser supports optional input folder and output root folder arguments,
    both defaulting to None to allow interactive prompts if not provided.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Auto organize images by date using exif metadata.")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=None,
        help="Source folder path where images were dumped (default: current folder if empty)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help=f"Output root folder where date folders are created (default: {P_PHOTOS_TRANSIENT_DEFAULT})",
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update metadata.json in output folder and all its first-level subfolders",
    )
    return parser


def read_json(filepath: Path) -> Union[Dict[str, Any], List[Any]]:
    """
    Read a JSON file from a given filepath and return its content.

    Args:
        filepath (Path): Path to the JSON file to read.

    Returns:
        Union[Dict[str, Any], List[Any]]: Parsed JSON data as a dictionary or list.
    """
    try:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (TypeError, JSONDecodeError) as _:
        print(f"{C_E}Couldn't read [{filepath}]")
        return {}


def save_json(filepath: Path, data: Dict[str, Any]) -> None:
    """
    Save a dictionary to JSON, converting datetime objects to ISO strings.

    Args:
        filepath (Path): Path to save the JSON file.
        data (Dict[str, Any]): Data to save.
    """

    def default_serializer(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return str(obj)

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=default_serializer)


def create_timestamp_from_time_string(
    time_str: Union[str, None], folder: Path, timezone: str = "Europe/Berlin"
) -> Dict[str, Any]:
    """
    Convert a hh:mm:ss time string into a timezone-aware datetime and UTC timestamp.

    Args:
        time_str (Union[str, None]): Time string in format hh:mm:ss (1–2 digits per part).
        folder (Path): Folder where gps_timestamp.json will be saved.
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
        today = datetime.date.today()
        dt_local = datetime.datetime(today.year, today.month, today.day, hour, minute, second, tzinfo=local_zone)
        dt_utc = dt_local.astimezone(datetime.timezone.utc)
        utc_str = dt_utc.isoformat()
        timestamp_ms = int(dt_utc.timestamp() * 1000)

        result = {"original": time_str, "utc": utc_str, "timestamp": timestamp_ms, "datetime": dt_utc}

        save_json(folder / F_TIMESTAMP_GPS, result)
        print(f"{C_H}Saved timestamp to {C_P}{folder / F_TIMESTAMP_GPS}{C_0}")
        return result

    except Exception as e:
        print(f"{C_E}Failed to parse time string: {e}{C_0}")
        return {}


def save_txt(filepath: Path, lines: Union[str, List[str]]) -> None:
    """
    Save a string or list of strings to a text file with exception handling.

    Args:
        filepath (Path): Path to save the file.
        lines (Union[str, List[str]]): Content to write. If string, converted to list.
    """
    if isinstance(lines, str):
        lines = [lines]

    try:
        with filepath.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{C_H}Saved text file: {C_P}{filepath}{C_0}")
    except Exception as e:
        print(f"{C_E}Failed to save file {filepath}: {e}{C_0}")


def extract_image_timestamp(filepath: Union[str, Path] = "") -> Dict[str, Any]:
    """
    Extract SubSecDateTimeOriginal from an image using exiftool and return timestamp info.

    Args:
        filepath (Union[str, Path]): Path to the image file. If empty, fallback logic is applied.

    Returns:
        Dict[str, Any]: Dictionary with keys:
            - "original": original timestamp string from EXIF
            - "utc": UTC timestamp string
            - "timestamp": UTC timestamp in milliseconds
            - "datetime": datetime.datetime object
            - "filename": absolute path to the image file
    """

    # Step 1: Resolve image path
    if not filepath:
        fallback_path = Path.cwd() / "gps.jpg"
        if fallback_path.exists():
            filepath = fallback_path
        else:
            jpg_files = list(Path.cwd().glob("*.jpg"))
            if not jpg_files:
                print(f"{C_E}No JPG files found in current directory.{C_0}")
                return {}
            print(f"{C_T}Select an image file to extract timestamp:{C_0}")
            for idx, file in enumerate(jpg_files):
                print(f"{C_I}[{idx}] {C_P}{file.name}{C_0}")
            try:
                choice = int(input(f"{C_Q}Enter number of file to use: {C_0}").strip())
                filepath = jpg_files[choice]
            except (ValueError, IndexError):
                print(f"{C_E}Invalid selection.{C_0}")
                return {}

    filepath = Path(filepath).resolve()
    if not filepath.exists():
        print(f"{C_E}File not found: {filepath}{C_0}")
        return {}

    # Step 2: Run exiftool extracting Original DateTime Original
    cmd = [CMD_EXIF, "-SubSecDateTimeOriginal", "-b", str(filepath)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        original = result.stdout.strip().replace(":", "-", 2)  # Normalize for parsing
        dt_obj = date_parser.parse(original)
        dt_utc = dt_obj.astimezone(datetime.timezone.utc)
        utc_str = dt_utc.isoformat()
        timestamp_ms = int(dt_utc.timestamp() * 1000)

        output = {
            "original": original,
            "utc": utc_str,
            "timestamp": timestamp_ms,
            "datetime": dt_utc,
            "filename": str(filepath),
        }

        # Save to gps_offset.json
        save_json(filepath.parent / F_TIMESTAMP_CAMERA, output)
        print(f"{C_H}GPS timestamp saved to {C_P}{filepath.parent / F_TIMESTAMP_CAMERA}{C_0}")
        return output

    except subprocess.CalledProcessError as e:
        print(f"{C_E}Exiftool failed: {e.stderr}{C_0}")
        return {}


def render_mini_timeline(gps_ts: int, cam_ts: int) -> None:
    """
    Render a mini timeline showing GPS and Camera timestamps and their offset.

    Args:
        gps_ts (int): GPS timestamp in milliseconds.
        cam_ts (int): Camera timestamp in milliseconds.
    """
    offset_sec = (cam_ts - gps_ts) / 1000
    total_width = 40
    midpoint = total_width // 2

    # Normalize positions
    if abs(offset_sec) > midpoint:
        scale = abs(offset_sec) / midpoint
        gps_pos = 0 if offset_sec > 0 else int(midpoint - offset_sec / scale)
        cam_pos = int(midpoint + offset_sec / scale) if offset_sec > 0 else midpoint
    else:
        gps_pos = midpoint
        cam_pos = int(midpoint + offset_sec)

    # Build timeline
    timeline = ["─"] * total_width
    timeline[gps_pos] = "🟦"  # GPS
    timeline[cam_pos] = "🟥"  # Camera

    print(f"\n{C_T}Mini Timeline:{C_0}")
    print(f"{C_PY}GPS 🟦{' ' * (gps_pos)}|{' ' * (cam_pos - gps_pos - 1)}🟥 Camera{C_0}")
    print(f"{C_H}{''.join(timeline)}{C_0}")
    print(f"{C_B}Offset: {offset_sec:.3f} seconds{C_0}")


def calculate_time_offset(path: Path = None, timezone: str = "Europe/Berlin") -> str:
    """
    Calculate time offset T_CAMERA - T_GPS in seconds.
    Deletes offset.env before writing new values.
    Saves both numeric and formatted hh:mm:ss offset.
    """
    import datetime
    from zoneinfo import ZoneInfo

    folder = path if path is not None else Path.cwd()
    offset_file = folder / F_OFFSET

    # Step 1: Delete existing offset.env
    if offset_file.exists():
        try:
            offset_file.unlink()
            print(f"{C_PY}Deleted existing {offset_file}{C_0}")
        except Exception as e:
            print(f"{C_E}Failed to delete {offset_file}: {e}{C_0}")

    # Step 2: Load camera and GPS timestamps
    camera_path = folder / F_TIMESTAMP_CAMERA
    gps_path = folder / F_TIMESTAMP_GPS

    camera_data = read_json(camera_path) if camera_path.exists() else {}
    gps_data = read_json(gps_path) if gps_path.exists() else {}

    if not camera_data:
        print(f"{C_E}Missing TIMESTAMP_CAMERA.json. Cannot compute offset.{C_0}")
        offset_ms = 0
    else:
        if not gps_data:
            print(f"{C_E}Missing TIMESTAMP_GPS.json. Please enter GPS time manually.{C_0}")
            time_str = input(f"{C_Q}Enter GPS time (hh:mm:ss): {C_0}").strip()
            try:
                parts = [int(p) for p in time_str.split(":")]
                while len(parts) < 3:
                    parts.append(0)
                hour, minute, second = parts[:3]
                local_zone = ZoneInfo(timezone)
                today = datetime.date.today()
                dt_local = datetime.datetime(
                    today.year, today.month, today.day, hour, minute, second, tzinfo=local_zone
                )
                dt_utc = dt_local.astimezone(datetime.timezone.utc)
                gps_ts = int(dt_utc.timestamp() * 1000)
                gps_data["timestamp"] = gps_ts
                gps_data["original"] = time_str
                gps_data["utc"] = dt_utc.isoformat()
                gps_data["datetime"] = dt_utc
            except Exception as e:
                print(f"{C_E}Failed to parse GPS time: {e}{C_0}")
                offset_ms = 0
        else:
            gps_ts = gps_data.get("timestamp", 0)

        cam_ts = camera_data.get("timestamp", 0)
        offset_ms = cam_ts - gps_ts
        print(f"{C_H}Camera Time: {C_P}{camera_data.get('original', 'N/A')}{C_0}")
        print(f"{C_H}GPS Time:    {C_P}{gps_data.get('original', 'N/A')}{C_0}")
        print(f"{C_H}Offset (s): {C_B}{offset_ms / 1000:.3f}{C_0}")
        render_mini_timeline(gps_ts, cam_ts)

    # Step 3: Format offset as hh:mm:ss
    offset_sec = int(offset_ms / 1000)
    sign = "-" if offset_sec < 0 else ""
    abs_sec = abs(offset_sec)
    hh = abs_sec // 3600
    mm = (abs_sec % 3600) // 60
    ss = abs_sec % 60
    offset_str = f"{sign}{hh:02}:{mm:02}:{ss:02}"

    # Step 4: Save to offset.env
    save_txt(offset_file, [f"OFFSET_SECONDS={offset_sec}", f"OFFSET_HMS={offset_str}"])
    print(f"{C_H}Saved offset [{offset_str}] to {C_P}{offset_file}{C_0}")
    return offset_str


def create_from_exiftool(input_folder: Path, output_root: Path) -> None:
    """
    Execute exiftool to extract metadata from image files in the input folder recursively.

    Runs exiftool with options to generate JSON metadata including specified image extensions,
    and writes the output to 'metadata.json' inside the output root folder.

    Args:
        input_folder (Path): Folder path containing images to analyze.
        output_root (Path): Folder where metadata.json will be saved.

    Prints:
        Status messages and exiftool progress output.
    """

    output_path = input_folder / "metadata.json"
    cmd = get_base_exiftool_cmd(input_folder)

    print(f"\n{C_T}### Running exiftool for metadata extraction in {C_P}{input_folder}{C_T}...{C_0}")

    with output_path.open("w", encoding="utf-8") as outfile:
        process = subprocess.Popen(cmd, stdout=outfile, stderr=subprocess.PIPE, text=True)

        # Stream exiftool progress to console
        for line in process.stderr:
            print(f"{C_PY}{line.strip()}{C_0}")

        process.wait()

        if process.returncode != 0:
            print(f"{C_E}Exiftool failed for {input_folder}{C_0}")
        else:
            print(f"{C_H}Metadata successfully saved to {C_P}{output_path}{C_0}")


def process_metadata_json(metadata_path: Path) -> Dict[str, dict]:
    """
    Process the metadata JSON file to build a dictionary keyed by last four digits of filenames.

    Extracts datetime from 'SubSecDateTimeOriginal', converts it to a datetime object,
    extracts date string in YYYYMMDD format, and organizes data for each image.

    Args:
        metadata_path (Path): Path to the metadata JSON file.

    Returns:
        Dict[str, dict]: Dictionary mapping 4-digit keys to metadata with keys:
                         'key', 'filename', 'datetime_created' (datetime object), and 'date' string.
    """
    raw_data = read_json(metadata_path)
    output_dict = {}
    if len(raw_data) == 0:
        return {}

    for entry in raw_data:
        try:
            source_file = entry["SourceFile"]
            dt_str = entry["Composite"]["SubSecDateTimeOriginal"]
            # transform dashes since they seem to lead to date
            # interpolation erorrs
            # 2025-10-06T19:03:19.400000+02:00
            dt_str = dt_str.replace(":", "-", 2)
            dt_obj = date_parser.parse(dt_str)
            date_str = dt_obj.strftime("%Y%m%d")
            filename = Path(source_file).name
            key = filename[-8:-4]  # last 4 digits as key
            output_dict[key] = {"key": key, "filename": filename, "datetime_created": dt_obj, "date": date_str}
        except Exception:
            # Skip entries missing required fields or malformed
            print(f"Error trying to parse {entry}")
            continue
    return output_dict


def update_metadata_in_all_subfolders(output_root: Path) -> None:
    """
    Run exiftool on all first-level subfolders of output_root to update metadata.json files.
    Skips the root folder itself.

    Args:
        output_root (Path): The root folder containing dated subfolders.
    """
    child_folders = [f for f in output_root.iterdir() if f.is_dir()]
    summary = []

    print(f"\n{C_T}### Updating metadata.json in {len(child_folders)} subfolders...{C_0}")
    for folder in child_folders:
        metadata_path = folder / "metadata.json"
        files = list(folder.glob("*.*"))
        file_count = len(files)

        print(f"\n{C_H}Running exiftool in: {C_P}{folder}{C_0}")
        cmd = get_base_exiftool_cmd(folder)
        with metadata_path.open("w", encoding="utf-8") as outfile:
            process = subprocess.Popen(cmd, stdout=outfile, stderr=subprocess.PIPE, text=True)
            for line in process.stderr:
                print(f"{C_PY}{line.strip()}{C_0}")
            process.wait()

        status = "✅ Success" if process.returncode == 0 else "❌ Failed"
        summary.append({"folder": folder.name, "file_count": file_count, "status": status})

    print(f"\n{C_T}### Metadata Update Summary:{C_0}")
    for idx, entry in enumerate(summary):
        print(
            f"{C_H}- {C_I}[{str(idx).zfill(2)}] {C_P}{entry['folder']}{C_H}: "
            f"{C_B}{entry['file_count']} files, {entry['status']}{C_0}"
        )


def save_processed_dict(output_dict: Dict[str, dict], save_path: Path) -> None:
    """
    Save the processed metadata dictionary to a JSON file.

    Converts all datetime objects to ISO 8601 strings for JSON serialization.

    Args:
        output_dict (Dict[str, dict]): Dictionary to save.
        save_path (Path): Path where the JSON file will be written.
    """
    output_serializable = {}
    for k, v in output_dict.items():
        out_val = v.copy()
        out_val["datetime_created"] = v["datetime_created"].isoformat()
        output_serializable[k] = out_val

    with save_path.open("w", encoding="utf-8") as f:
        json.dump(output_serializable, f, indent=2)


def extract_number_key(filename: str) -> Union[str, None]:
    """
    Extract the last four digits of the last numerical sequence found in a filename.

    Args:
        filename (str): The filename string to search.

    Returns:
        Union[str, None]: The extracted four-digit key, or None if no number found.
    """

    numbers = re.findall(r"\d+", filename)
    if not numbers:
        return None
    last_number = numbers[-1]
    return last_number[-4:] if len(last_number) >= 4 else last_number


def create_date_folders(output_root: Path, date_list: List[str]) -> None:
    """
    Create directories named by dates in YYYYMMDD format inside the output root folder.

    Args:
        output_root (Path): Root folder where date folders should be created.
        date_list (List[str]): List of date strings (YYYYMMDD).
    """
    for date_str in date_list:
        folder_path = output_root / date_str
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)


def show_progress(num_moved: int, total: int) -> None:
    """
    Display a progress bar on the terminal for file moving operations.

    The progress bar uses colored block emojis and shows percentage and count.

    Args:
        num_moved (int): Number of files moved so far.
        total (int): Total number of files to move.
    """
    percent = num_moved / total if total else 1.0
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
        progressbar = green_block * 10 + yellow_block * (blocks_done - 10) + blue_block * (blocks_total - blocks_done)
    else:
        progressbar = green_block * 10 + yellow_block * 4 + orange_block * 4 + red_block * 2

    percent_display = int(percent * 100)
    sys.stdout.write(f"\r{C_T}Progress: {progressbar} {percent_display}% {C_I}({num_moved}/{total}){C_0}")
    sys.stdout.flush()


def move_files_by_date(input_folder: Path, output_root: Path, file_dict: Dict[str, dict]) -> List[str]:
    """
    Move image files from input folder to dated subfolders in output root based on metadata keys.

    Uses the last four digits extracted from filenames to find the corresponding date folder.

    Args:
        input_folder (Path): Folder containing image files to move.
        output_root (Path): Root folder where dated folders exist or will be created.
        file_dict (Dict[str, dict]): Dictionary mapping keys to image metadata.

    Returns:
        List[str]: List of filenames that could not be moved due to missing key in dictionary.
    """
    files = list(input_folder.glob("*.*"))
    total_files = len(files)
    moved_count = 0
    errors = []

    date_list = list(set(entry["date"] for entry in file_dict.values()))
    create_date_folders(output_root, date_list)

    for i, file_path in enumerate(files, start=1):
        key = extract_number_key(file_path.name)
        if key and key in file_dict:
            date_folder = output_root / file_dict[key]["date"]
            dest = date_folder / file_path.name
            try:
                shutil.move(str(file_path), str(dest))
                moved_count += 1
            except Exception:
                errors.append(file_path.name)
        else:
            errors.append(file_path.name)
        show_progress(i, total_files)
    print()  # newline after progress bar
    return errors


def summarize_and_update_metadata(output_root: Path, date_list: List[str]) -> List[Dict[str, Union[str, int]]]:
    """
    For each YYYYMMDD folder in output_root, count the files and rerun exiftool to export metadata.json.
    Displays exiftool progress and output during execution.
    """
    summary = []

    for date_str in date_list:
        folder_path = output_root / date_str
        if folder_path.exists() and folder_path.is_dir():
            files = list(folder_path.glob("*.*"))
            file_count = len(files)
            metadata_path = folder_path / "metadata.json"

            print(f"\n{C_T}### Writing Metadata: {C_P}{folder_path}{C_T} ---")
            print(f"Found {C_I}{file_count}{C_T} files. Running exiftool...{C_0}")

            cmd = get_base_exiftool_cmd(folder_path)

            with metadata_path.open("w", encoding="utf-8") as outfile:
                process = subprocess.Popen(cmd, stdout=outfile, stderr=subprocess.PIPE, text=True)

                # Stream stderr (exiftool progress and messages) to the console in real time
                for line in process.stderr:
                    print(f"{C_PY}{line.strip()}{C_0}")

                process.wait()

                if process.returncode != 0:
                    print(f"{C_E}Exiftool failed in folder {folder_path}{C_0}")

            summary.append({"date": date_str, "file_count": file_count})

    return summary


def main() -> None:
    """
    Main function that orchestrates reading arguments, running exiftool,
    processing metadata, moving files, updating metadata in date folders,
    and printing results.

    Interactively prompts for inputs if no arguments are specified.
    """
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.update:
        output_root = args.output
        if output_root is None:
            outp = input(
                f"{C_Q}Enter output root folder path for update (default {P_PHOTOS_TRANSIENT_DEFAULT}): {C_0}"
            ).strip()
            output_root = Path(outp) if outp else P_PHOTOS_TRANSIENT_DEFAULT
        else:
            output_root = Path(output_root)
        if not output_root.exists() or not output_root.is_dir():
            print(f"{C_E}Output folder {output_root} not found or invalid.{C_0}")
            return
        update_metadata_in_all_subfolders(output_root)
        return  # Exit after update

    # Determine input folder
    input_folder = args.input
    if input_folder is None:
        inp = input(f"{C_Q}Enter input folder path (default current folder): {C_0}").strip()
        if inp:
            input_folder = Path(inp)
        else:
            input_folder = Path.cwd()
            # input_folder = P_IMAGE_DUMP_DEFAULT
    else:
        input_folder = Path(input_folder)

    if not input_folder.exists() or not input_folder.is_dir():
        print(f"{C_E}Input folder {input_folder} not found or invalid.{C_0}")
        return

    # Determine output root folder
    output_root = args.output
    if output_root is None:
        outp = input(f"{C_Q}Enter output root folder path (default {P_PHOTOS_TRANSIENT_DEFAULT}): {C_0}").strip()
        if outp:
            output_root = Path(outp)
        else:
            output_root = P_PHOTOS_TRANSIENT_DEFAULT
    else:
        output_root = Path(output_root)

    if not output_root.exists():
        output_root.mkdir(parents=True, exist_ok=True)

    # Run exiftool to generate metadata.json for input folder
    create_from_exiftool(input_folder, output_root)

    metadata_path = input_folder / "metadata.json"
    if not metadata_path.exists():
        print(f"{C_E}Metadata file not found. Exiftool may have failed.{C_0}")
        return

    # Process metadata.json
    file_dict = process_metadata_json(metadata_path)
    save_processed_dict(file_dict, input_folder / "file_dump.json")
    print(f"{C_PY}Processed metadata saved as file_dump.json in input folder.{C_0}")

    # Move files by date
    errors = move_files_by_date(input_folder, output_root, file_dict)

    if errors:
        print(f"{C_E}The following files could not be moved:{C_0}")
        for efile in errors:
            print(f"{C_E} - {efile}{C_0}")
    else:
        print(f"{C_PY}All files moved successfully.{C_0}")

    # Summarize folders and update metadata.json in each dated folder
    date_list = list(set(entry["date"] for entry in file_dict.values()))
    summary = summarize_and_update_metadata(output_root, date_list)
    print(f"\n{C_T}### Summary of moved files per date (in {output_root} ):{C_0}")
    for idx, entry in enumerate(summary):
        print(
            f"{C_H}- {C_I}[{str(idx).zfill(2)}] {C_P}[{entry['date']}]{C_H}, Files moved:{C_B} {entry['file_count']}{C_0}"
        )


if __name__ == "__main__":
    main()
