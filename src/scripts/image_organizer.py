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

V6

rewrite calculate_time_offset, so that it also will write the gps_data dict to a
file using the Persistence.save_txt function. also refactor the generation of the output
dict in extract_image_timestamp and calculate_time_offset into a separate method

... more iterations ...

V5 - Additional Functions on getting the URL
Not documented prompts. some parts were also copied over from tools repo

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

import sys
import os
import re
import argparse

# import json
from json import JSONDecodeError
import datetime
import shutil
import subprocess

# import traceback
from pathlib import Path
from typing import Any, Dict, List, Union, Tuple, Optional
from zoneinfo import ZoneInfo

# from configparser import ConfigParser
from dateutil import parser as date_parser

# ANSI color codes
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F
from config.myenv import MY_CMD_EXIFTOOL, MY_P_PHOTO_DUMP, MY_P_PHOTOS_TRANSIENT
from libs.helper import Persistence, GeoLocation, CmdRunner, Transformer, Helper

# Paths from environemt
# Define image suffixes and default paths
IMAGE_SUFFIXES = ["jpg", "jpeg", "raf", "dng"]
# suffixes use in EXIFTOOL Comands
SUFFIX_ARGS = []
for ext in IMAGE_SUFFIXES:
    SUFFIX_ARGS.extend(["-ext", ext])


# EXIFTOOL https://exiftool.org/

# Note in the BAT Files you need to activate CHCP 65001 to get the right characters in output
CMD_EXIFTOOL = MY_CMD_EXIFTOOL

# 1. EXIFTOOL command to get the timestamp creation date of an image
CMD_EXIFTOOL_GET_DATE = [CMD_EXIFTOOL, "-SubSecDateTimeOriginal", "-b"]

# 2. EXIFTOOL command to export metadata
CMD_EXIFTOOL_EXPORT_METADATA = [CMD_EXIFTOOL, "-r", "-g", "-c", "'%.6f'", "-progress50", "-json"] + SUFFIX_ARGS

# 3. EXIFTOOL command to geotag images based on a gps track
# https://exiftool.org/geotag.html
# exiftool -progress50 -json -jpg -tif -geosync=00:00:00 -geotag mygps.gpx <file/path>
CMD_EXIFTOOL_GEOTAG = [CMD_EXIFTOOL, "-progress50", "-json"] + SUFFIX_ARGS

# 4. EXIFTOOL command to export existing GPS Coordinates as reverse Geo (addresses) from images as json in german
# Reverse Geotag Coordinates > Address:
# https://exiftool.org/geolocation.html
# https://exiftool.org/geolocation.html#Geotag
# WRITE https://exiftool.org/geolocation.html#Write
# Shows the geolocations as json file when there are GPS Coordinates available
# exiftool -api geolocation "-geolocation*" -lang de -json <file/path>
CMD_EXIFTOOL_GEOTAG = [CMD_EXIFTOOL, "-api", "geolocation", "-lang", "de", "-progress50", "-json"] + SUFFIX_ARGS

#
# https://exiftool.org/Shift.html
# https://exiftool.org/#shift
# exiftool "-AllDates+=0:0:0 0:0:42" -overwrite_original yourfile.jpg

# Write the Reverse GeoInfo from GPS Coordinates into a file
# exiftool "-geolocate=5.6429,5.9374" test.jpg

# EMPTY ALL exiftool  -all:all= empty0.jpg
# EXIFTOOL CREATE GPS Coordinates using
# exiftool "-DateTimeOriginal=2025:10:14 09:00:00" filename.jpg
# exiftool -GPSLatitude*=48.00 -GPSLongitude*=9.00 -GPSAltitude=100 "-gpsdatestamp<${datetimeoriginal}" "-gpstimestamp<${datetimeoriginal}"  empty0.jpg
# adjust for UTC -1 or 2
# OFFSET needs to be either +1 or +2 (utc_time + offset = local time) depending on daylight saving day
# exiftool -GPSLatitude*=48.00 -GPSLongitude*=9.00 -GPSAltitude=100 "-gpsdatestamp<${datetimeoriginal}+01:00" "-gpstimestamp<${datetimeoriginal}+01:00"  empty0.jpg
# MAybe also add Date Time Created From DateToimeCreated


# TODO
# https://exiftool.org/forum/index.php?topic=12620.0
# Your basic command would be (no plus signs, those aren't used with Coordinates)
# exiftool -GPSLatitude=40.6892 -GPSLatitudeRef=N -GPSLongitude=-74.0445 -GPSLongitudeRef=W -GPSAltitude=10 -GPSAltitudeRef="Above Sea Level" FILE
# There are two tags for each coordinate that needs to be set because EXIF holds the GPS number and direction separately.
# But exiftool is very flexible and the inputs can just be numbers, which can be useful with scripts
# exiftool -GPSLatitude=40.6892 -GPSLatitudeRef=40.6892 -GPSLongitude=-74.0445 -GPSLongitudeRef=-74.0445 -GPSAltitude=10 -GPSAltitudeRef=10 FILE
# And even better, you can condense this by using wildcards
# exiftool -GPSLatitude*=40.6892 -GPSLongitude*=-74.0445 -GPSAltitude*=10 FILE
# TODO_ extract all geo goordinates into a json using
# exiftool -gps:all -j -n -json *.jpg => this will give entries of type
# {
#   "SourceFile": "test.jpg",
#   "GPSVersionID": "2 3 0 0",
#   "GPSLatitudeRef": "N",
#   "GPSLatitude": 49.1426516231194,
#   "GPSLongitudeRef": "E",
#   "GPSLongitude": 8.69249434206389,
#   "GPSAltitudeRef": 0,
#   "GPSAltitude": 178,
#   "GPSTimeStamp": "15:22:52.5",
#   "GPSDateStamp": "2025:08:31"
# }
# =>


# TODO IMPLEMENT create a waypoint file from geotagged images using a template
# 5. EXIFTOOL create a waypoint file from geotagged images using a template
# https://exiftool.org/geotag.html#Inverse
# the template is stored \templates\exiftool_wpt.fmt
# exiftool -fileOrder gpsdatetime -ext jpg -p exiftool_wpt.fmt . > out.gpx
CMD_EXIFTOOL_CREATE_WAYPOINTS = [CMD_EXIFTOOL, "-fileOrder", "gpsdatetime", "-ext", "jpg", "-p"]
# exiftool_wpt.fmt . > out.gpx

P_PHOTO_DUMP_DEFAULT = Path(MY_P_PHOTO_DUMP)
P_PHOTOS_TRANSIENT_DEFAULT = Path(MY_P_PHOTOS_TRANSIENT)

# Timestamp files to calculate offset
# T_CAMERA - T_GPS = T_OFFSET
# default image for image containing camera timestamp
F_TIMESTAMP_IMG_DEFAULT = "gps.jpg"
F_TIMESTAMP_GPS = "timestamp_gps.json"
F_TIMESTAMP_CAMERA = "timestamp_camera.json"
F_OFFSET_ENV = "offset.env"
F_OFFSET_SECS_ENV = "offset_sec.env"
F_OSM_LAT_LON_ENV = "osm_lat_lon.env"
F_GPX_ENV = "gpx_merged.env"
F_GPX_MERGED = "gpx_merged.gpx"
F_TMP_FILES = [F_TIMESTAMP_CAMERA, F_TIMESTAMP_GPS, F_OFFSET_ENV, F_OFFSET_SECS_ENV, F_OSM_LAT_LON_ENV]


def generate_timestamp_dict(source: Union[str, datetime.datetime], filepath: Optional[Path] = None) -> Dict[str, Any]:
    """
    Generate a standardized timestamp dictionary from a string or datetime object.

    Args:
        source (Union[str, datetime.datetime]): Raw timestamp string or datetime object.
        filepath (Optional[Path]): Optional path to include in output.

    Returns:
        Dict[str, Any]: Dictionary with keys: original, utc, timestamp, datetime, [filename]
    """
    if isinstance(source, str):
        normalized = source.replace(":", "-", 2)
        dt_obj = date_parser.parse(normalized)
        original = source
    else:
        dt_obj = source
        original = dt_obj.isoformat()

    dt_utc = dt_obj.astimezone(datetime.timezone.utc)
    utc_str = dt_utc.isoformat()
    timestamp_ms = int(dt_utc.timestamp() * 1000)

    output = {
        "original": original,
        "utc": utc_str,
        "timestamp": timestamp_ms,
        "datetime": dt_utc,
    }
    if filepath:
        output["filename"] = str(filepath)
    else:
        output["filename"] = "no filename"

    return output


def read_geosync_from_env(p_source: Path) -> str:
    """reads the offset string from the"""

    # get the geosync offset (previously written), with a default of 00:00:00
    f_offset = p_source.joinpath(F_OFFSET_ENV)
    lines = Persistence.read_txt_file(f_offset)
    t_offset = "+00:00:00" if len(lines) == 0 else lines[0]
    return f"-geosync={t_offset}"


def get_exiftool_cmd_export_meta_recursive(input_folder: Path) -> list:
    """creates the exiftool command to export image data as json"""

    # command to export all exifdata in groups as json for given suffixes
    # progress is shown every 50 images
    # the c command is to format gps coordinates as decimals
    exif_cmd = CMD_EXIFTOOL_EXPORT_METADATA.copy()
    exif_cmd.append(str(input_folder))
    return exif_cmd


def get_exiftool_create_gps_metadata_from_gpx(p_source: Path) -> bool:
    """creates the exiftool command to create gpx data in image files

    Returns:
     bool: True if the command succeeded, False otherwise.
    """

    # use current path or input path
    p_work = p_source if p_source.is_dir() else Path().resolve()
    f_gpx_merged = p_work.joinpath(F_GPX_MERGED)

    f_gpx_merged = f_gpx_merged if f_gpx_merged.is_file() else None
    if f_gpx_merged is None:
        print(f"{C_H}No gpx file {f_gpx_merged} found, skip processing of creating gps based on gpx{C_0}")
        return

    # get the geosync offset (previously written), with a default of 00:00:00
    geosync = read_geosync_from_env(p_source)

    # command to geotag all elements in folder using an offset
    exif_cmd = CMD_EXIFTOOL_GEOTAG.copy()
    additional_params = [geosync, "-geotag", f_gpx_merged, str(p_source)]
    exif_cmd.append(additional_params)
    success = CmdRunner.run_cmd_and_print(exif_cmd)

    return success


def prepare_collateral_files(p_source: Path) -> None:
    """Prepare collateral files centrally.
    - Delete Collateral Files first
    - Merge GPX Files if there are any => F_GPX_ENV
    - Read Calibration Image  => F_TIMESTAMP_CAMERA
    - Read / Input GPS Time from Image => F_TIMESTAMP_GPS
    - Calculate Time Offset: F_TIMESTAMP_CAMERA / F_TIMESTAMP_GPS => F_OFFSET_ENV
    - Extract lat lon default from OSM links => F_LAT_LON_ENV
    """

    # use current path or input path
    p_work = p_source if p_source.is_dir() else Path().resolve()
    # 0. Delete any temporary files
    cleanup_env_files(p_source)
    # 1. Create Merged GPS, if not already present
    f_merged_gpx = GeoLocation.merge_gpx(p_work, F_GPX_ENV)
    # 2. Select Reference File and extract timestanp of camera
    timstamp_dict_camera = extract_image_timestamp(p_source)
    # 3. Now Get the GPS Timestamp (as seen on the image of the previous image)
    time_offset = calculate_time_offset(p_work)
    # 4. Extract the OSM Link as default GPS Coordinates
    osm_coordinates = GeoLocation.get_openstreetmap_coordinates_from_folder(F_OSM_LAT_LON_ENV, p_source)


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
            # note: is case sensitive
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
    cmd = CMD_EXIFTOOL_GET_DATE.copy()
    cmd.append(str(filepath))

    print(f"{C_T}Running exiftool command:{C_0} {cmd}")
    success = CmdRunner.run_cmd_and_print(cmd)
    if not success:
        print(f"{C_E}Exiftool command failed.{C_0}")
        return {}

    # Step 3: Capture output manually (if needed, could be redirected or parsed differently)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        original = result.stdout.strip()
        output = generate_timestamp_dict(original, filepath)
        Persistence.save_json(filepath.parent / F_TIMESTAMP_CAMERA, output)
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


def show_image(f_image: Path) -> None:
    """opens the camera image for display"""
    # read the file path
    if not f_image.is_file():
        print(f"{C_E}Can't open file [{f_image}]{C_0}")
        return
    print(f"\n{C_T}### Opening File in default image program: {C_F}[{f_image}]{C_0}")
    # open the image in the default viewer
    cmd = ["start", str(f_image)]
    CmdRunner.run_cmd_and_print(cmd)


def cleanup_env_files(path: Path = None):
    """CleanUp all ENV files."""
    # use current path or input path
    p_work = path if path.is_dir() else Path().resolve()
    _ = [p_work.joinpath(f).unlink(missing_ok=True) for f in F_TMP_FILES]


def calculate_time_offset(p_source: Path = None, timezone: str = "Europe/Berlin") -> str:
    """
    Calculate the time offset between camera and GPS timestamps and save results.
    T_GPS + T_OFFSET = T_CAMERA

    This function computes the time offset in seconds between the camera timestamp
    (from `timestamp_camera.json`) and the GPS timestamp (from `timestamp_gps.json`).
    If the GPS timestamp is missing, the user is prompted to enter a time string
    (hh:mm:ss), which is converted to a UTC timestamp using the provided timezone.

    The function saves:
    - `timestamp_camera.json`: camera timestamp dictionary
    - `timestamp_gps.json`: GPS timestamp dictionary
    - `offset.env`: containing OFFSET_SECONDS and OFFSET_HMS (hh:mm:ss format)

    Args:
        path (Path, optional): Directory containing timestamp files. Defaults to current directory.
        timezone (str, optional): Timezone for interpreting manual GPS input. Defaults to "Europe/Berlin".

    Returns:
        str: The formatted offset string in hh:mm:ss format.
    """
    folder = p_source if p_source else Path.cwd()
    offset_file = folder / F_OFFSET_ENV
    offset_file_sec = folder / F_OFFSET_SECS_ENV
    gps_json_file = folder / F_TIMESTAMP_GPS
    camera_json_file = folder / F_TIMESTAMP_CAMERA

    # Step 1: Remove existing offset file
    if offset_file.exists():
        try:
            offset_file.unlink()
            print(f"{C_PY}Deleted existing {offset_file}{C_0}")
        except Exception as e:
            print(f"{C_E}Failed to delete {offset_file}: {e}{C_0}")

    # Step 2: Load or generate timestamps
    camera_data = Persistence.read_json(camera_json_file) if camera_json_file.exists() else {}
    # read gps data if already saved
    gps_data = Persistence.read_json(gps_json_file) if gps_json_file.exists() else {}

    if not camera_data:
        print(f"{C_E}Missing TIMESTAMP_CAMERA.json. Offset will be set to zero.{C_0}")
        offset_ms = 0
    else:
        if not gps_data:
            print(f"{C_E}Missing TIMESTAMP_GPS.json. Please enter GPS time manually{C_0}")
            f_image = Path(camera_data.get("filename", "NA"))
            if f_image.is_file:
                print(f"{C_H}Show Image [{f_image}]{C_0}")
                show_image(f_image)

            time_str = input(f"{C_Q}Enter GPS time [hh:mm:ss](blank to skip): {C_0}").strip()
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
                gps_data = generate_timestamp_dict(dt_local)
                gps_data["original"] = time_str  # preserve user input
            except Exception as e:
                print(f"{C_E}Invalid GPS Time, no offset applied{C_0}")
                offset_ms = 0

        gps_ts = gps_data.get("timestamp", 0)
        cam_ts = camera_data.get("timestamp", 0)
        offset_sec = int((cam_ts - gps_ts) / 1000)
        offset_str = Helper.format_seconds_offset(offset_sec)

        print(f"{C_H}Camera Time: {C_P}{camera_data.get('original', 'N/A')}{C_0}")
        print(f"{C_H}GPS Time: {C_P}{gps_data.get('original', 'N/A')}{C_0}")
        print(f"{C_H}Offset (s): {C_B}{offset_sec}sec / {offset_str}{C_0}")
        render_mini_timeline(gps_ts, cam_ts)

    # Step 4: Save all outputs
    Persistence.save_json(camera_json_file, camera_data)
    Persistence.save_json(gps_json_file, gps_data)
    Persistence.save_txt(offset_file, offset_str)
    Persistence.save_txt(offset_file_sec, str(offset_sec))

    print(f"{C_H}Saved camera timestamp to {C_P}{camera_json_file}{C_0}")
    print(f"{C_H}Saved GPS timestamp to {C_P}{gps_json_file}{C_0}")
    print(f"{C_H}Saved offset [{offset_str}] to {C_P}{offset_file}{C_0}")
    print(f"{C_H}Saved offset sec [{offset_sec}] to {C_P}{offset_file_sec}{C_0}")
    return offset_str


def resolve_gps_track(p_source: Path | None, f_gps_track: Path | str | None) -> Path:
    """Determines the GPX Track.
    In following order:
    - Merged GPX Path
    - Run Merge Operation, then return Merged GPX Path
    - None if there are no GPX Files
    """
    p_input = Path.cwd()
    if p_source:
        p_input = Path(p_source)
    f_gps = Path(f_gps_track)
    # directly use the provided path
    if f_gps.is_file():
        return f_gps
    # 1. Check if there is a merged file already
    f_gps_merged = p_source.joinpath(F_GPX_ENV)
    if f_gps_merged.is_file():
        return f_gps_merged
    # 2. Merge Any GPX Files into the standard one
    f_gps_merged = GeoLocation.merge_gpx(p_input, F_GPX_MERGED)
    if f_gps_merged:
        f_gps_merged = Path(f_gps_merged)
    return f_gps_merged


def exiftool_add_gpsmeta_from_gps(p_source: Path, f_gps_track: str | Path | None) -> None:
    """
    Execute exiftool to add GPS Coordinates from a GPX Track.
    """
    p_cwd = os.getcwd()
    f_track = resolve_gps_track(p_source, f_gps_track)
    if f_track is None:
        return
    # run in project path
    os.chdir(str(p_source))
    # clean up existing tmp files, get timestamps to calculate offset, get osm coordinates
    prepare_collateral_files(p_source)
    f_track_name = f_track.name

    # read the geosync offset
    geosync = read_geosync_from_env(p_source)
    print(f"{C_T}### Using GPS Track {C_F}[{f_track}] (Offset {geosync}){C_0}")

    # exiftool -geosync=+00:00:00 -geotag track.gpx *.jpg
    os.chdir(p_cwd)


def exiftool_create_metadata_recursive(p_source: Path) -> None:
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

    output_path = p_source / "metadata.json"
    cmd = get_exiftool_cmd_export_meta_recursive(p_source)

    success = CmdRunner.run_cmd_and_stream(cmd, output_path)
    if success:
        print(f"{C_H}Metadata successfully saved  {C_P}{output_path}{C_0}")
    else:
        print(f"{C_E}Exiftool failed for command [{p_source}{C_0}]")


def get_unprocessed_files(p_source: Union[str, Path], f_out: Optional[Union[str, Path]] = None) -> Dict[str, List[str]]:
    """
    Identify image files in the folder that lack corresponding backup files.

    For each file with a suffix in IMAGE_SUFFIXES, check if a backup file
    with the same name and suffix "<suffix>_original" exists. If not, add
    the full path to the output dictionary under "files_unprocessed".

    Args:
        folder (Union[str, Path]): Path to the folder to scan.
        f_out (Optional[Union[str, Path]]): Optional path or filename to save the output dictionary.

    Returns:
        Dict[str, List[str]]: Dictionary with key "files_unprocessed" and list of unmatched file paths.

    PROMPT
    Now add a function get_unprocessed_files that does the following:
    - For a given path it reads all files with the given suffix <suffix> defined in IMAGE_SUFFIXES
    - Check if for such a file a backup file having the same name and the suffix <suffix>_original exists
    - if it doesn't exist, add the full path of this file to an output dict under the attribute "files_unprocessed"
    - as output return this dictionary
    - Add an input param f_out to the function: if it's None, do nothing. if it is a string or path, save this dictionary under
    the path given by f_out. if it's just a name and not an absolute path, then use the current directory as save path

    """
    p_source = Path(p_source).resolve()
    output_dict = {"files_unprocessed": []}

    for suffix in IMAGE_SUFFIXES:
        pattern = f"*.{suffix}"
        for file_path in p_source.glob(pattern):
            backup_name = file_path.stem + f".{suffix}_original"
            backup_path = p_source / backup_name
            if not backup_path.exists():
                output_dict["files_unprocessed"].append(str(file_path))

    # Save output if f_out is provided
    if f_out:
        f_out_path = Path(f_out)
        if not f_out_path.is_absolute():
            f_out_path = Path.cwd() / f_out_path
        Persistence.save_json(f_out_path, output_dict)

    return output_dict


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
    raw_data = Persistence.read_json(metadata_path)
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


def update_metadata_recursive(p_root: Path) -> None:
    """
    Run exiftool on all first-level subfolders of output_root to update metadata.json files.
    Skips the root folder itself.

    Args:
        output_root (Path): The root folder containing dated subfolders.
    """
    child_folders = [f for f in p_root.iterdir() if f.is_dir()]
    summary = []

    print(f"\n{C_T}### Updating metadata.json in {len(child_folders)} subfolders...{C_0}")
    for folder in child_folders:
        metadata_path = folder / "metadata.json"
        files = list(folder.glob("*.*"))
        file_count = len(files)

        print(f"\n{C_H}Running exiftool in: {C_P}{folder}{C_0}")
        cmd = get_exiftool_cmd_export_meta_recursive(folder)

        success = CmdRunner.run_cmd_and_stream(cmd, metadata_path)
        status = "✅ Success" if success else "❌ Failed"
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

    Persistence.save_json(save_path, output_serializable)


def extract_number_key(filename: str) -> Union[str, None]:
    """
    Extract the last four digits of the last numerical sequence found in a filename
    (usual patterrn for image files)

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

            cmd = get_exiftool_cmd_export_meta_recursive(folder_path)

            success = CmdRunner.run_cmd_and_stream(cmd, metadata_path)
            if not success:
                print(f"{C_E}Exiftool failed in folder {folder_path}{C_0}")

            summary.append({"date": date_str, "file_count": file_count})

    return summary


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
        "-ps",
        "--p_source",
        type=str,
        default=None,
        help="Source folder path where images were dumped (default: current folder if empty)",
    )
    parser.add_argument(
        "-po",
        "--p_output",
        type=str,
        default=None,
        help=f"Output root folder where date folders are created (default: {P_PHOTOS_TRANSIENT_DEFAULT})",
    )
    parser.add_argument(
        "-aju",
        "--action_meta_json_update_recursive",
        action="store_true",
        help="Update metadata.json in output folder and all its first-level subfolders",
    )
    parser.add_argument(
        "-ap",
        "--action_prepare_geo_meta",
        action="store_true",
        help="Prepare collateral files for geo tagging",
    )

    return parser


def action_prepare_geo_meta(args: argparse.Namespace) -> bool | None:
    "Prepare Metadata to be used for geo tagging"
    if args.action_prepare_geo_meta is not True:
        return None

    # validate and get the source path
    p_source = validate_p_source(args)
    if p_source is None:
        p_source = Path().resolve()

    prepare_collateral_files(p_source)
    return True


def action_update_metadata_recursive(args: argparse.Namespace) -> bool | None:
    """Update the exiftool metadata json in all child folder"""
    if args.action_meta_json_update_recursive is not True:
        return None

    p_root = args.p_source
    if p_root is None:
        outp = input(
            f"{C_Q}Enter source root folder path for update (default {P_PHOTOS_TRANSIENT_DEFAULT}): {C_0}"
        ).strip()
        p_root = Path(outp) if outp else P_PHOTOS_TRANSIENT_DEFAULT
    else:
        p_root = Path(p_root)

    if not p_root.exists() or not p_root.is_dir():
        print(f"{C_E}Output folder {p_root} not found or invalid.{C_0}")
        return False

    update_metadata_recursive(p_root)

    return True


def validate_p_source(args: argparse.Namespace) -> Path | None:
    """validates input folder if required"""
    # Determine input folder
    p_source = args.p_source
    if p_source is None:
        inp = input(f"{C_Q}Enter input folder path (default current folder): {C_0}").strip()
        if inp:
            p_source = Path(inp)
        else:
            p_source = Path.cwd()
    else:
        p_source = Path(p_source)

    if not p_source.exists() or not p_source.is_dir():
        print(f"{C_E}Input folder {p_source} not found or invalid.{C_0}")
        return None

    return p_source


def cmd_validate_p_output(args: argparse.Namespace) -> Path | None:
    """validates output folder if required"""
    # Determine input folder
    p_output = args.p_output
    if p_output is None:
        outp = input(f"{C_Q}Enter output folder path (default current folder): {C_0}").strip()
        if outp:
            p_output = Path(outp)
        else:
            p_output = Path.cwd()
    else:
        p_output = Path(p_output)

    if not p_output.exists() or not p_output.is_dir():
        print(f"{C_E}Input folder {p_output} not found or invalid.{C_0}")
        return None

    return p_output


def main() -> None:
    """
    Main function that orchestrates reading arguments, running exiftool,
    processing metadata, moving files, updating metadata in date folders,
    and printing results.

    Interactively prompts for inputs if no arguments are specified.
    """
    success: bool | None = False
    parser = build_arg_parser()
    args = parser.parse_args()

    # now performa all actions as controlled by input params

    # 1. write the metadata.json for all child paths
    success = action_update_metadata_recursive(args)
    # 2. prepare the metadata for a dedicated output folder
    success = action_prepare_geo_meta(args)

    # Determine output root folder
    # output_root = args.output
    # if output_root is None:
    #     outp = input(f"{C_Q}Enter output root folder path (default {P_PHOTOS_TRANSIENT_DEFAULT}): {C_0}").strip()
    #     if outp:
    #         output_root = Path(outp)
    #     else:
    #         output_root = P_PHOTOS_TRANSIENT_DEFAULT
    # else:
    #     output_root = Path(output_root)
    # if not output_root.exists():
    #     output_root.mkdir(parents=True, exist_ok=True)

    # Run exiftool to generate metadata.json for input folder
    # exiftool_create_metadata_recursive(input_folder, output_root)

    # metadata_path = input_folder / "metadata.json"
    # if not metadata_path.exists():
    #     print(f"{C_E}Metadata file not found. Exiftool may have failed.{C_0}")
    #     return

    # # Process metadata.json
    # file_dict = process_metadata_json(metadata_path)
    # save_processed_dict(file_dict, input_folder / "file_dump.json")
    # print(f"{C_PY}Processed metadata saved as file_dump.json in input folder.{C_0}")

    # # Move files by date
    # errors = move_files_by_date(input_folder, output_root, file_dict)

    # if errors:
    #     print(f"{C_E}The following files could not be moved:{C_0}")
    #     for efile in errors:
    #         print(f"{C_E} - {efile}{C_0}")
    # else:
    #     print(f"{C_PY}All files moved successfully.{C_0}")

    # # Summarize folders and update metadata.json in each dated folder
    # date_list = list(set(entry["date"] for entry in file_dict.values()))
    # summary = summarize_and_update_metadata(output_root, date_list)
    # print(f"\n{C_T}### Summary of moved files per date (in {output_root} ):{C_0}")
    # for idx, entry in enumerate(summary):
    #     print(
    #         f"{C_H}- {C_I}[{str(idx).zfill(2)}] {C_P}[{entry['date']}]{C_H}, Files moved:{C_B} {entry['file_count']}{C_0}"
    #     )


if __name__ == "__main__":
    main()
