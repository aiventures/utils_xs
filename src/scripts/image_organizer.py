#!/usr/bin/env python3
"""Moves Image according to their timestamps.

# HOWTO
- Geotracker images should be called gps.jpg
- osm url files name doens't matter. if there are multiple you'll be asked
- gpx file will be merged into one gpx if there are multiple gpx files


TODO
- Refactor to Instance Classes
- Add the cli command to create the track from images (jpgs only)
- Add the cli command to move file to folders without creating exifs
- Add a cli command to rename files
- Add cli command to create geolocation data in images including description

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
corresponding DateTime object for the datetime string - add a dedicated save_json
function to store the json file receiving filename and data as dict. Also adjust datetime
attribute fields to be able to be stored as json (not leading to errors) -
save this dict as gps_offset.json in the path where the file is located

V1 - update F_METADATA_EXIF for output folders
add another function:  check the --output folder and all its first level children folders and apply
the run_exiftool on each of those folders to update the F_METADATA_EXIF files there
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
- In path P_IMAGE_DUMP_DEFAULT, execute the command F_CMD_EXIF -r -g -ext jpg -ext jpeg -json . > P_OUTPUT_ROOT/F_METADATA_EXIF
  - For F_CMD_EXIF, use the path to the exiftool executable
  - Export rhe F_METADATA_EXIF to the folder stored in P_OUTPUT_ROOT
  - For the set of -ext parameters use the suffixes defined in the image_suffixes list
  - the P_OUTPUT_ROOT/F_METADATA_EXIF file will be a json list of entries (one entry per image file).
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
    - read the P_OUTPUT_ROOT/F_METADATA_EXIF (using a read_json function) into a dict file_dict
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
- Add ANSI COLOR CODES so it is possible to use colored output using f strings like f"{C_T}text".
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

from __future__ import annotations
import argparse
import datetime
import json
import os
import re
import traceback
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

# ANSI color codes
from config.colors import C_0, C_B, C_E, C_F, C_H, C_I, C_L, C_P, C_PY, C_Q, C_S, C_T, C_W

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


from libs.geo_meta_transformer import GeoMetaTransformer
from libs.exiftool_fields import ExifToolFieldsMapper, IPTC

from libs.geo import (
    CONFIG_F_GPX_MERGED,
    # GeotrackerGPXDATA,
    CONFIG_F_GPX_MERGED_ENV,
    CONFIG_F_GPX_MERGED_JSON,
    CONFIG_F_METADATA,
    CONFIG_F_METADATA_ENV,
    CONFIG_F_METADATA_EXIF,
    CONFIG_F_METADATA_EXIF_ENV,
    CONFIG_F_METADATA_GEO_REVERSE,
    CONFIG_F_METADATA_GEO_REVERSE_ENV,
    CONFIG_F_OFFSET_ENV,
    CONFIG_F_OFFSET_SECS_ENV,
    CONFIG_F_OSM,
    # OpenStretMapConfiguration,
    CONFIG_F_OSM_ENV,
    CONFIG_F_TIMESTAMP_CAMERA,
    CONFIG_F_TIMESTAMP_CAMERA_ENV,
    CONFIG_F_TIMESTAMP_GPS,
    CONFIG_F_TIMESTAMP_GPS_ENV,
    CONFIG_F_TIMESTAMP_IMG,
    CONFIG_F_TIMESTAMP_IMG_ENV,
    CONFIG_OFFSET_SECS,
    CONFIG_OFFSET_STR,
    CONFIG_TIMESTAMP_CAMERA,
    CONFIG_TIMESTAMP_GPS,
    DATETIME,
    ELEVATION,
    FILENAME,
    FILEPATH,
    F_GPX_MERGED,
    # F_GPX_MERGED_JSON,
    F_GPX_MERGED_ENV,
    F_METADATA,
    F_METADATA_ENV,
    F_METADATA_EXIF,
    F_METADATA_EXIF_ENV,
    F_METADATA_GEO_REVERSE,
    F_OFFSET_ENV,
    F_OFFSET_SECS_ENV,
    F_OSM,
    F_OSM_ENV,
    F_TIMESTAMP_CAMERA,
    F_EXIFTOOL_IMPORT,  # Metadata Dump To IMport Metadata using Exiftool
    F_TIMESTAMP_GPS,
    # ImagecontainingthetimestampandtheGPSImage,
    # Timestampfilestocalculateoffset,
    # T_CAMERA-T_GPS,
    # defaultimageforimagecontainingcameratimestamp,
    F_TIMESTAMP_IMG_DEFAULT,
    F_TIMESTAMP_IMG_ENV,
    # DATETIME_ORIGINAL,
    # DATETIME_ADJUSTED,
    FILES,
    # FILENAME,
    FILES_ENV,
    # LAT_LON_ORIGIN,
    GPS_TRACK,
    TRACK,
    HEARTRATE,
    IMAGE_GEO_INFO,
    IMAGE_REVERSE_GEO_INFO,
    # OFFSET_STR,
    # OFFSET_CAM,
    # OFFSET_GPS,
    LAT_LON,
    METADATA_EXIF,
    METADATA_EXIFTOOL,
    # METADATA_IPTC,
    METADATA_OSM,
    # METADATA_GEO,
    OFFSET,
    OFFSET_SECS,
    # TIMESTAMP_IMAGE,
    # GPS_METADATA,
    TEMPERATURE,
    TIMESTAMP_UTC,
    TIMEZONE,
    TIMEZONE_DEFAULT,
    # EXIFTOOL METADATA IMPORT DEFINITIONS
    # EXIFTOOL_METADATA_IMPORT,
    CONFIG_F_EXIFTOOL_IMPORT,
    CONFIG_F_EXIFTOOL_IMPORT_ENV,
)

from libs.binary_sorter import BinarySorter
from libs.helper import CmdRunner, Helper, Persistence
from libs.reverse_geo import ReverseGeo
from libs.exiftool import ExifTool, CMD_EXIFTOOL
from libs.geo import IMAGE_SUFFIXES

MY_P_PHOTO_DUMP: Path = Path(ENV_DICT["MY_P_PHOTO_DUMP"])
P_PHOTO_OUTPUT_ROOT: Path = Path(ENV_DICT["MY_P_PHOTO_OUTPUT_ROOT"])

FILETYPE_RAW: list = ["arw", "dng", "raf"]
FILETYPE_IMG: list = ["jpg", "jpeg", "png"]
FILETYPE_TMP: list = ["env", "tmp", "tif", "tiff", "dop", "jpg_original"]
FILES_DO_NOT_MOVE: list = ["metadata.json", "exiftool_import.json", "gps.jpg", "gpx_merged.gpx"]
FILES_DELETE: list = ["timestamp_gps.json", "timestamp_camera.json"]
FILESUFFIX_DO_NOT_MOVE = ["url"]

# Collected Geo Information alongside with origin info
GEOTRACK_INFO: Dict = {
    "geotrack_origin": None,
    "metadata_geo": None,
    "gps_info": {
        "datetime_camera_exif": None,
        "offset": 0,
        "datetime_camera_utc": None,
        "datetime_gps_utc": None,
        "timestamp_camera": None,
        "timestamp_gps": None,
        "timestamp_diff": None,
    },
}

GEOTRACK_ORIGIN_OSM = "osm"
GEOTRACK_ORIGIN_GPX = "gpx"

# general setup of the metadata json containin all relevant information
CONFIG_METADATA: Dict = {
    DATETIME: None,  # creation date of this file
    TIMESTAMP_UTC: None,  # creation date timestamp
    FILES_ENV: {  # indirection/hardwired: insread of using file names directly, use an indirection via env
        CONFIG_F_METADATA_ENV: F_METADATA_ENV,
        CONFIG_F_METADATA_EXIF_ENV: F_METADATA_EXIF_ENV,
        CONFIG_F_TIMESTAMP_IMG_ENV: F_TIMESTAMP_IMG_ENV,  # file ref to image of the GPTRACKER
        CONFIG_F_OSM_ENV: F_OSM_ENV,
        CONFIG_F_GPX_MERGED_ENV: F_GPX_MERGED_ENV,
        CONFIG_F_TIMESTAMP_CAMERA_ENV: F_TIMESTAMP_CAMERA,  # file ref to camera offset dates
        CONFIG_F_TIMESTAMP_GPS_ENV: F_TIMESTAMP_GPS,  # file ref to gps offset dates
        CONFIG_F_OFFSET_ENV: F_OFFSET_ENV,  # file ref to image offset in form /-+hh:mm:ss
        CONFIG_F_OFFSET_SECS_ENV: F_OFFSET_SECS_ENV,  # file ref to image offset in seconds
        CONFIG_F_METADATA_GEO_REVERSE_ENV: F_METADATA_GEO_REVERSE,  # file to GEO REVEERSE DATA
        CONFIG_F_EXIFTOOL_IMPORT_ENV: F_EXIFTOOL_IMPORT,  # fileref to json containing metadata to be used for exiftool image import
    },
    # F_OFFSET_ENV = "offset.env"
    # F_OFFSET_SECS_ENV = "offset_sec.env"
    # if files are found then the None will be replaced by real path
    FILES: {
        CONFIG_F_METADATA: None,  # All Metadata In One File (= This File)
        CONFIG_F_METADATA_EXIF: None,  # Image Metadata
        CONFIG_F_TIMESTAMP_IMG: None,  # GPS TRACKER Image (from CONFIG_F_TIMESTAMP_IMG_ENV)
        CONFIG_F_TIMESTAMP_CAMERA: None,
        CONFIG_F_TIMESTAMP_GPS: None,
        CONFIG_F_OSM: None,  # OSM URL Link
        CONFIG_F_GPX_MERGED: None,  # Link to merged GPX Files
        CONFIG_F_GPX_MERGED_JSON: None,  # Link to merged GPX JSON
        CONFIG_F_METADATA_GEO_REVERSE: None,  # Georeverse Metadata
        CONFIG_F_EXIFTOOL_IMPORT: None,  # metadata json containing import metadata
    },
    OFFSET: {
        CONFIG_OFFSET_STR: "+00:00:00",  # Offset as -+hh:mm:ss
        CONFIG_OFFSET_SECS: 0,  # absolute offset T_GPS+T_OFFSET = T_CAM in seconds
        CONFIG_TIMESTAMP_CAMERA: {},  # Offset JSON for Camera
        CONFIG_TIMESTAMP_GPS: {},  # Offset JSON for GPS
    },
    METADATA_OSM: {},  # Geo Metadata retrieved via EXIFTOOL and copied from F_OSM_INFO
    GPS_TRACK: {},  # GPS Track, copy of F_GPX_MERGED_JSON
    METADATA_EXIF: {},  # Copied from F_METADATA_EXIF / but with FILENAME as key
    IMAGE_GEO_INFO: {},  # metadata for each file, structure see below
    IMAGE_REVERSE_GEO_INFO: {},  # reverse geo info
}


class GeoLocation:
    """Helper for Geolocation Handling."""

    @staticmethod
    def create_gpx_header(soup: BeautifulSoup) -> Tag:
        """Create the header for the GPX Track"""
        gpx_tag = soup.new_tag("gpx")
        gpx_tag.attrs = {
            "creator": "Garmin Connect",
            "version": "1.1",
            "xmlns": "http://www.topografix.com/GPX/1/1",
            "xmlns:ns2": "http://www.garmin.com/xmlschemas/GpxExtensions/v3",
            "xmlns:ns3": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/11.xsd",
        }
        return gpx_tag

    @staticmethod
    def create_dict_from_gpx(p_source: Union[str, Path], f_output: Union[str, Path] | None) -> Dict[str, Any]:
        """
        Parses a GPX file and returns its contents as a structured JSON-like dictionary.
        Also saves the result to a JSON file.

        Args:
            p_source (Union[str, Path]): Path to the input GPX file.
            f_output (Union[str, Path]): Path or filename for the output JSON file.

        Returns:
            Dict[str, Any]: Dictionary with keys:
                - "header": attributes from the <gpx> tag
                - "metadata": flattened metadata from <metadata>
                - "track": dict of track points keyed by 13-digit UTC timestamp (int, milliseconds)
        """
        p_source = Path(p_source).resolve()
        f_output = Path(f_output)
        if not f_output.is_absolute():
            f_output = p_source / f_output

        with p_source.open("r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml")

        # Extract header attributes from <gpx>
        gpx_tag = soup.find("gpx")
        header = {k.replace(":", "_"): v for k, v in gpx_tag.attrs.items()}

        # Extract metadata
        metadata_tag = soup.find("metadata")
        metadata = {}
        if metadata_tag:
            for child in metadata_tag.find_all(recursive=False):
                metadata[child.name] = child.text.strip()

        # Extract and flatten track points
        track = {}
        for trkpt in soup.find_all("trkpt"):
            trkpt_data = {k: v for k, v in trkpt.attrs.items()}
            for child in trkpt.find_all(recursive=False):
                if child.name == "extensions":
                    for ext in child.find_all():
                        for sub in ext.find_all():
                            flat_key = f"{child.name}_{ext.name}_{sub.name}".replace(":", "_")
                            val = sub.text.strip()
                            trkpt_data[flat_key.lower()] = float(val) if val.replace(".", "", 1).isdigit() else val
                else:
                    val = child.text.strip()
                    trkpt_data[child.name] = float(val) if child.name == "ele" else val

            # Convert time to 13-digit UTC timestamp
            time_str = trkpt_data.get("time")
            if time_str:
                dt = DateTime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                utc_timestamp = int(dt.timestamp() * 1000)
                trkpt_data["utc_timestamp"] = utc_timestamp
                track[utc_timestamp] = trkpt_data  # Use int key

        # Compose final JSON structure
        gpx_json = {"header": header, "metadata": metadata, "track": track}

        # Eventually Save to file
        if f_output:
            with f_output.open("w", encoding="utf-8") as f:
                json.dump(gpx_json, f, indent=4, ensure_ascii=False)

        return gpx_json

    @staticmethod
    def merge_gpx(
        p_source: Union[str, Path], f_output: Union[str, Path], create_json: bool = True, overwrite: bool = True
    ) -> Optional[str]:
        """
        Merge multiple GPX files in a folder into a single GPX file.

        - Uses metadata from the file with the earliest <metadata><time>
        - Collects all <trkpt> segments and sorts them by <time>
        - Saves the merged GPX to f_output and if create_json is set, also create the
          json respresentation

        Args:
            folder (Union[str, Path]): Folder containing GPX files.
            f_output (Union[str, Path]): Output file path or filename.

        PROMPT

        in the GeoLocation class, add a static function merge_gpx, that will do the following:
        * Use the following sample as spec for the GPX geo tracking file
        <?xml version="1.0" encoding="UTF-8"?>
        <gpx creator="Garmin Connect" version="1.1"
        xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/11.xsd"
        xmlns:ns3="http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
        xmlns="http://www.topografix.com/GPX/1/1"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns2="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
        <metadata>
            <link href="connect.garmin.com">
            <text>Garmin Connect</text>
            </link>
            <time>2025-08-31T13:30:57.000Z</time>
        </metadata>
        <trk>
            <name>Radfahren</name>
            <type>cycling</type>
            <trkseg>
            <trkpt lat="49.13321242667734622955322265625" lon="8.7750278413295745849609375">
                <ele>171.8000030517578125</ele>
                <time>2025-08-31T13:31:10.000Z</time>
                <extensions>
                <ns3:TrackPointExtension>
                    <ns3:hr>129</ns3:hr>
                </ns3:TrackPointExtension>
                </extensions>
            </trkpt>
            <trkpt lat="49.13316900841891765594482421875" lon="8.7750531546771526336669921875">
                <ele>171.8000030517578125</ele>
                <time>2025-08-31T13:31:11.000Z</time>
                <extensions>
                <ns3:TrackPointExtension>
                    <ns3:hr>129</ns3:hr>
                </ns3:TrackPointExtension>
                </extensions>
            </trkpt>
            </trkseg>
        </trk>
        </gpx>
        Now create the following function to create amerged gpx file
        * get a path location as input and a parameter f_output as save filepath for a new gpx file
        * collect all files with the GPX extension in that path
        * Use beautiful soup to parse the gpx files according to given specification
        * copy the metadata part from the file that has the earliest <metadata><time> timestamp
        * from all collected files, extract all <trkpt> segments, sort them ascending by <time>, and add all of them in the <trk><trkseg> section
        * save this new merged data as f_output (if f_output is not an absolute path, save it in the current path)
        """
        p_source = Path(p_source).resolve()
        f_output = Path(f_output)
        if not f_output.is_absolute():
            f_output = p_source / f_output

        # skip if merged path already exists, you need to manually delete it again if not present
        if f_output.is_file():
            if overwrite:
                os.remove(str(f_output))
            else:
                printt(f"File {C_F}[{f_output}]{C_T} already exists")
                return

        gpx_files = sorted(p_source.glob("*.gpx"))
        if not gpx_files:
            printe(f"No GPX files found in {C_F}{p_source}")
            return None

        metadata_time_map = {}
        trkpt_elements = []

        check_for_duplicates = True if len(gpx_files) > 1 else False

        for gpx_file in gpx_files:
            with gpx_file.open("r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "xml")

            metadata = soup.find("metadata")
            time_tag = metadata.find("time") if metadata else None
            time_val = DateTime.max
            if time_tag:
                try:
                    time_val = DateTime.fromisoformat(time_tag.text.replace("Z", "+00:00"))
                except Exception:
                    pass
            metadata_time_map[gpx_file] = (time_val, metadata)

            trkpts = soup.find_all("trkpt")
            trkpt_elements.extend(trkpts)

        # Sort trkpts by <time>
        def trkpt_time(trkpt):
            time_tag = trkpt.find("time")
            try:
                return DateTime.fromisoformat(time_tag.text.replace("Z", "+00:00"))
            except Exception:
                return DateTime.max

        try:
            trkpt_elements.sort(key=trkpt_time)
        except TypeError as _:
            printe(" Error Occured merging GPX tracks (mixing time tags?)")
            printpy(traceback.format_exc())

            return None

        # Create new GPX structure
        soup_out = BeautifulSoup(features="xml")
        gpx_tag = GeoLocation.create_gpx_header(soup_out)

        soup_out.append(gpx_tag)

        # Add earliest metadata
        earliest_file = min(metadata_time_map.items(), key=lambda x: x[1][0])[0]
        metadata_tag = metadata_time_map[earliest_file][1]
        if metadata_tag:
            gpx_tag.append(metadata_tag)

        # Add track and track segment
        trk_tag = soup_out.new_tag("trk")
        name_tag = soup_out.new_tag("name")
        name_tag.string = "Merged GPX Track"
        type_tag = soup_out.new_tag("type")
        type_tag.string = "cycling"
        trk_tag.append(name_tag)
        trk_tag.append(type_tag)

        trkseg_tag = soup_out.new_tag("trkseg")

        seen_timestamps = set()
        for trkpt in trkpt_elements:
            if check_for_duplicates:  # only necessary when merging multiple files
                time_tag = trkpt.find("time")
                if time_tag:
                    try:
                        timestamp = DateTime.fromisoformat(time_tag.text.replace("Z", "+00:00"))
                        if timestamp in seen_timestamps:
                            printw(f"Found duplicate timestamp in tracks {C_H}{timestamp}")
                            continue  # Skip duplicate
                        seen_timestamps.add(timestamp)
                    except Exception:
                        pass  # If time is malformed, include it anyway
            trkseg_tag.append(trkpt)

        trk_tag.append(trkseg_tag)
        gpx_tag.append(trk_tag)

        # Save to file
        soup_str = soup_out.prettify()
        Persistence.save_txt(f_output, soup_str)

        printt(f"Merged GPX saved to {C_H}{f_output}")
        if create_json:
            f_output_json = f_output.parent.joinpath(f"{f_output.stem}.json")
            _ = GeoLocation.create_dict_from_gpx(p_source=f_output, f_output=f_output_json)
            printt(f"Merged GPX JSON saved to {C_H}{f_output_json}")
        return str(f_output)

    @staticmethod
    def latlon_from_osm_url(url: str) -> Optional[Tuple[float, float]]:
        """
        Extracts latitude and longitude from an OpenStreetMap URL with 7-digit float precision.
        https://www.openstreetmap.org/#map=xx/lat/lon
        https://www.openstreetmap.org/search?query=qd#map=xx/lat/lon"

        Args:
            url (str): OpenStreetMap URL containing #map=zoom/lat/lon

        Returns:
            Optional[Tuple[float, float]]: (latitude, longitude) if found, else None
        """
        match = re.search(r"#map=\d+/([\-0-9.]+)/([\-0-9.]+)", url)
        if match:
            lat = round(float(match.group(1)), 7)
            lon = round(float(match.group(2)), 7)
            return lat, lon
        return None

    @staticmethod
    def create_openstreetmap_shortcut(lat: float, lon: float) -> str:
        """Shorcut Link"""
        shortcut_lines = ["[InternetShortcut]", f"URL=https://www.openstreetmap.org/#map={lat:.7f}/{lon:.5f}"]
        shortcut = "\n".join(shortcut_lines)
        return shortcut

    @staticmethod
    def get_openstreetmap_coordinates_from_folder(
        file: str, folder: Optional[Path] = None
    ) -> Optional[Tuple[float, float]]:
        """
        Reads all .url files in a folder, filters for OpenStreetMap links, and returns lat/lon coordinates.
        If multiple links are found, prompts the user to select one.
        Also writes the selected lat,lon to F_LAT_LON in the same folder.

        Args:
            folder (Optional[Path]): Folder to scan. Defaults to current directory.

        Returns:
            Optional[Tuple[float, float]]: Selected coordinates or None if no match found.
        """
        folder = folder or Path.cwd()
        if not folder.exists() or not folder.is_dir():
            printe("Invalid folder: {folder}")
            return None

        env_file = folder / file
        if env_file.exists():
            try:
                env_file.unlink()
                printt(f"Deleted existing {env_file}")
            except Exception as e:
                printe(f"Failed to delete {env_file}: {e}")

        url_files = list(folder.glob("*.url"))
        output = {}

        exiftool = ExifTool()
        for idx_f, f in enumerate(url_files, 1):
            output_per_file = {}
            url = Persistence.read_internet_shortcut(str(f))

            if url and "openstreetmap.org" in url.lower():
                coords = GeoLocation.latlon_from_osm_url(url)
                output_per_file = exiftool.get_reverse_geoinfo(latlon=coords, file=f, index=idx_f)
                output[idx_f] = output_per_file
            else:
                continue

        if not output:
            printw(f"No OpenStreetMap links with coordinates found in {folder}")
            return None

        if len(output) == 1:
            selected = next(iter(output.values()))
            printt(f"Found one OpenStreetMap link: {C_P}{selected['file']}")
        else:
            printt("Multiple OpenStreetMap links found:")
            for idx, info in output.items():
                coords = info.get("lat_lon", ("NA", "NA"))
                geo_info = info.get("geo_info", "NA")
                file = info.get("file", "NA")
                print(
                    f"{C_I}[{idx}] {C_P}{file}{C_T} → lat: {coords[0]:.5f}, lon: {coords[1]:.5f}{C_0},info: {geo_info} {C_0}"
                )

            try:
                choice = int(inputc("Enter number of file to use").strip())
                selected = output[choice]
            except (ValueError, IndexError):
                printe("Invalid selection. No coordinates returned.")
                return None

        try:
            Persistence.save_json(env_file, selected)
            printh(f"Saved Geo Info to {C_P}{env_file}")
        except Exception as e:
            printe(f"Failed to write coordinates: {e}")

        return selected

    @staticmethod
    def get_gpx_file_from_folder(file, folder: Optional[Path] = None) -> Optional[str]:
        """
        Scans a folder for .gpx files and writes the selected filename to F_GPX_ENV.
        Deletes any existing F_GPX_ENV file before writing.


        Args:
            folder (Optional[Path]): Folder to scan. Defaults to current directory.

        Returns:
            Optional[str]: Selected GPX filename or None if no file was selected.
        """
        folder = folder or Path.cwd()
        if not folder.exists() or not folder.is_dir():
            printe("Invalid folder: {folder}")
            return None

        env_file = folder / file
        if env_file.exists():
            try:
                env_file.unlink()
                printt(f"Deleted existing {env_file}")
            except Exception as e:
                printe(f"Failed to delete {env_file}: {e}")

        gpx_files = list(folder.glob("*.gpx"))
        if not gpx_files:
            printe("No GPX files found in {folder}")
            return None

        if len(gpx_files) == 1:
            selected = gpx_files[0].name
            try:
                env_file.write_text(selected + "\n", encoding="utf-8")
                printh(f"Saved GPX filename [{selected}] to {C_P}{env_file}")
            except Exception as e:
                printe(f"Failed to write GPX filename: {e}")
            return selected

        printt("Multiple GPX files found:")
        for idx, f in enumerate(gpx_files):
            print(f"{C_I}[{idx}] {C_P}{f.name}{C_0}")

        try:
            choice = int(inputc("Enter number of file to use").strip())
            selected = gpx_files[choice].name
            env_file.write_text(selected + "\n", encoding="utf-8")
            printh(f"Saved GPX filename [{selected}] to {C_P}{env_file}")
            return selected
        except (ValueError, IndexError):
            printe("Invalid selection. No GPX file saved.")
            return


class ImageOrganizer:
    """Class to process image metadata"""

    def __init__(
        self,
        # actions to be performed
        action_prepare_meta: bool = True,
        action_prepare_transform: bool = True,
        action_change_metadata: bool = True,
        # collateral inforamtion
        path: Path | str = None,
        timezone_s: str = TIMEZONE_DEFAULT,
        max_timediff: int = 300,
        encoding: str = "latin1",
        show_gps_image: bool = True,
        use_reverse_geo: bool = True,
        overwrite_reverse_geo: bool = False,
        f_metadata: str = F_METADATA,
        f_metadata_exif: str = F_METADATA_EXIF,
        f_reverse_geo: str = F_METADATA_GEO_REVERSE,
        f_gpx_merged: str = F_GPX_MERGED,
        f_exiftool_import: str = F_EXIFTOOL_IMPORT,
        cmd_exiftool: str = CMD_EXIFTOOL,
        language: str = "de",
        cmd_exiftool_output: bool = True,
        auto_confirm: bool = False,
    ):
        self._timezone: str = timezone_s
        # get the work path / by default currrent path
        _path = Path.cwd()
        if path is not None:
            _path = Path(path)
        if not _path.is_dir():
            printe("[ImageOrganizer] No valid path {_path}")
            return None
        self._path: Path = _path.absolute()

        # add actions
        self._action_prepare_meta = action_prepare_meta
        self._action_prepare_transform = action_prepare_transform
        self._action_change_metadata = action_change_metadata

        # setting the file names
        # variables to keep
        self._show_gps_image: bool = show_gps_image
        # use the reverse geo service
        self._use_reverse_geo: bool = use_reverse_geo
        # overwrite the reverse geo info file containing nominatim data
        self._overwrite_reverse_geo: bool = overwrite_reverse_geo
        # all metadata
        self._metadata: Dict = None
        # maximum time difference between EXIF Date and GPS Date allowed in seconds
        self._max_timediff: int = max_timediff
        # file encoding might lead to issues on windows if not latin1 or cp1252
        # utf-8 struggles in my case
        self._encoding: str = encoding
        # language for metadata
        self._language = language
        # name of the file containin the exif data export from exiftool
        self._f_metadata_exif: str = f_metadata_exif
        # name of the metadata file containing everything
        self._f_metadata: str = f_metadata
        # name of the reverse geo file
        self._f_reverse_geo: str = f_reverse_geo
        # name of the merged gpx file
        self._f_gpx_merged: str = f_gpx_merged
        # name of the metadatafile to be used for changing exiftdata
        self._f_exiftool_import = f_exiftool_import
        # path to exiftool executable
        self._cmd_exiftool = cmd_exiftool
        # output of exiftool
        self._cmd_exiftool_output = cmd_exiftool_output
        # auto confirm user input
        self._auto_confirm: bool = auto_confirm
        # get an exiftool instance
        self._exiftool = self._create_exiftool()

    def _create_exiftool(self, encoding: str = None, progress: int = 10) -> Optional[ExifTool]:
        """creates an exiftool instance or None if it couldn't be instanciated"""
        encoding_ = encoding if encoding is not None else self._encoding
        exiftool = ExifTool(
            path=self._path,
            encoding=encoding_,
            language=self._language,
            f_exiftool=self._cmd_exiftool,
            f_gpx_merged=self._f_gpx_merged,
            show_output=self._cmd_exiftool_output,
            progress=progress,
        )

        exiftool = exiftool if exiftool.is_instanciated else None
        if exiftool is None:
            printe("[Image Organizer] couldn't instanciate Exiftool")
        return exiftool

    @property
    def exiftool(self) -> Optional[ExifTool]:
        """getter for exiftool"""
        return self._exiftool

    @staticmethod
    def get_img_geo_from_track(metadata_exif: Dict, gpx_sorter: BinarySorter, time_offset_secs: int = 0) -> Dict | None:
        """Gets the geo reverse infomration using gpx track"""
        geo_info: Dict = None
        _file_name = "unknown"
        _file_name_absolute = "unknown"
        out_str = "🖼️   "
        _offset = -time_offset_secs
        _track_info = None
        _lat_lon = None

        track_info: Dict = deepcopy(GEOTRACK_INFO)
        track_info["geotrack_origin"] = GEOTRACK_ORIGIN_GPX

        try:
            _gps_info = track_info["gps_info"]
            _file_name = metadata_exif.get("File", {}).get("FileName", "No Filename Found")
            _file_name_absolute = metadata_exif.get("SourceFile", "Unknown")

            out_str += f"{C_F}[{_file_name}] {C_0}"

            # Parse the date time string like: 2025:08:31 16:04:26.73+02:00
            # Note the timezone is already there and will be considered
            _datetime = metadata_exif["Composite"]["SubSecDateTimeOriginal"]
            _gps_info["datetime_camera_exif"] = _datetime
            _gps_info["offset"] = _offset

            out_str += f" {C_H}{_datetime}/{C_Q}{_offset}"
            print(out_str)
            out_str = ""

            # T[GPS] + T[OFFSET]= T[CAMERA] => so we need to subtract from camera time
            _datetime_utc: DateTime = Helper.get_datetime_from_format_string(
                _datetime, "%Y:%m:%d %H:%M:%S.%f", offset=-time_offset_secs
            )
            out_str += f"{C_H}    📷 {_datetime_utc.isoformat()}"
            _cam_timestamp_utc = _datetime_utc.timestamp() * 1000
            _gps_info["datetime_camera_utc"] = _datetime_utc.isoformat()
            _gps_info["timestamp_camera"] = int(_cam_timestamp_utc)

            # get the gpx entry
            _track_info = gpx_sorter.get_data_by_value(_cam_timestamp_utc)
            if _track_info:
                _track_data = _track_info["data"]
                _track_timestamp_utc = _track_data["utc_timestamp"]
                # 6 digits should be enough, accuracy on 10cm level ...
                # https://docs.mapbox.com/help/dive-deeper/geojson-coordinate-precision/
                # https://rapidlasso.de/how-many-decimal-digits-for-storing-longitude-latitude/
                _lat_lon = [round(float(_track_data["lat"]), 6), round(float(_track_data["lon"]), 6)]
                _gps_date_time = DateTime.fromtimestamp(_track_timestamp_utc / 1000, tz=timezone.utc)
                _timestamp_diff = round((_cam_timestamp_utc - _track_timestamp_utc) / 1000, 3)
                out_str += f" | 🛰️  ({_gps_date_time.isoformat()}) |\n    {C_W}🔢 Diff: [{_timestamp_diff}]sec,  "
                out_str += f"{C_PY}🌏 {_lat_lon}{C_0}"
                _gps_info["datetime_gps_utc"] = _gps_date_time.isoformat()
                _gps_info["timestamp_gps"] = _track_timestamp_utc
                _gps_info["timestamp_diff"] = _timestamp_diff
                print(out_str)

            else:
                printw("Metadata File [{_file_name}] has out of bounds time [{_datetime}]")

        except (ValueError, KeyError) as e:
            printe(f"Metadata File [{_file_name}] has unexpected format, Error: {e}")

        if not os.path.isfile(_file_name_absolute):
            printe("File [{_file_name_absolute}] doesn't exist.")
            return

        if _lat_lon is None:
            printw(f"File [{_file_name_absolute}] no coordinates found.")
            return

        # return the dict
        exiftool = ExifTool()
        geo_info = exiftool.get_reverse_geoinfo(_lat_lon, _file_name_absolute, 1)
        track_info["metadata_geo"] = geo_info

        return track_info

    def process_reverse_geo_metadata(
        self,
        overwrite: bool = False,
    ) -> Dict:
        """Based on the metadata file, collect metadata for all images"""
        if self._metadata is None:
            printe("No Metadata available, did you run merge_metadata ?")
            return {}

        if self._use_reverse_geo is False:
            # skip processing, return the existing metadata
            printd("[image_organizer] process_reverse_geo_metadata Skip getting reverse geodata")
            return self._metadata

        _metadata = self._metadata
        _path = self._path

        # get the data from buffered data already
        _f_reverse_geo = _path.joinpath(self._f_reverse_geo)
        _reverse_geo_metadata: Dict = None

        # load the buffered data if there
        _reverse_geo = ReverseGeo(f_reverse_geo=_f_reverse_geo, load=True)

        # delete existing file if there
        if overwrite:
            _reverse_geo.delete()

        # read reverse info for osm link if existent
        _metadata_osm = _metadata.get(METADATA_OSM, {})
        _gps_track = _metadata.get(GPS_TRACK, {}).get("track", {})
        _reverse_geo_osm = None
        _osm_filename = None
        if len(_metadata_osm) > 0:
            _lat_lon = _metadata_osm.get(LAT_LON)
            _osm_filename = Path(_metadata_osm.get("file", "osmlink_not_there.url")).name
            _reverse_geo_osm = _reverse_geo.read_geo_info(_lat_lon, ext_key=_osm_filename)
            # additionally write the metadta to the osm segment
            _metadata_osm[IMAGE_REVERSE_GEO_INFO] = _reverse_geo_osm

        if _reverse_geo_metadata is None:
            printh("🌍 Reading reverse geo info from reverse geo service")

            # it will be assumed the geo info was collected prior to calling this function
            image_geo_info_dict: Dict = _metadata.get(IMAGE_GEO_INFO, {})
            if len(image_geo_info_dict) == 0:
                printw("[ImageOrganizer] the metadata segment image_geo_info is empty")
                return _metadata

            # read reverse info for all images and format a neat output
            for _filename, _geo_info in image_geo_info_dict.items():
                # print(json.dumps(_geo_info, indent=4))
                extra = {FILENAME: _filename}
                add_text = None
                timestamp = _geo_info["gps_info"]["timestamp_gps"]
                if timestamp is not None:
                    extra[TIMESTAMP_UTC] = int(timestamp)
                    time_zone = _geo_info["metadata_geo"]["time_zone"]
                    extra[TIMEZONE] = time_zone
                    datetime_s = Helper.format_timestamp(timestamp, time_zone)
                    extra[DATETIME] = datetime_s
                    add_text = f"⌚ {C_Q}{datetime_s}"
                    # also try to get the geotrack info from track
                    _track_data = _gps_track.get(str(timestamp), {})
                    # print(json.dumps(_track_data, indent=4))
                    # get elevation and heart rate as well
                    _ele = _track_data.get("ele")
                    _hr = _track_data.get("extensions_trackpointextension_hr")
                    _temperature = _track_data.get("extensions_trackpointextension_atemp")
                    if _ele:
                        extra[ELEVATION] = int(_ele)
                        add_text += f"{C_L} ⛰️ {extra[ELEVATION]}m"
                    if _hr:
                        extra[HEARTRATE] = int(_hr)
                        add_text += f"{C_E} ❤️ {extra[HEARTRATE]}"
                    if _temperature:
                        extra[TEMPERATURE] = round(float(_temperature), 1)
                        add_text += f"{C_E} 🌡️ {extra[TEMPERATURE]}°C"

                _lat_lon = _geo_info["metadata_geo"]["lat_lon"]
                _ = _reverse_geo.read_geo_info(_lat_lon, ext_key=_filename, add_text=add_text, extra=extra)

        _reverse_geo_metadata = _reverse_geo.get_geo_info_dict(as_ext_key=True)
        # update the metadata parts
        _metadata[FILES][CONFIG_F_METADATA_GEO_REVERSE] = str(_f_reverse_geo)
        _metadata[IMAGE_REVERSE_GEO_INFO] = _reverse_geo_metadata
        # save the metadata in a separate file
        _reverse_geo.save()
        return _metadata

    def _process_geo_metadata(self) -> Optional[Dict]:
        """Based on the metadata file, collect metadata for all images"""
        _path = self._path
        if self._metadata is None:
            printe("No Metadata available, did you run merge_metadata ?")
            return

        _metadata = self._metadata
        # get the metadata dict either from parameters or from file
        if not _metadata:
            _f_metadata_json = _path.joinpath(self._f_metadata)
            if not _f_metadata_json.is_file():
                printe("Metadata File [{_f_metadata_json}] wasn't found ")
                return
            _metadata = Persistence.read_json(_f_metadata_json)
        # get dict fields
        _offset = _metadata[OFFSET]
        _gps_track = _metadata[GPS_TRACK]
        _track_dict = _gps_track.get("track", {})
        _has_gps_track = True if len(_track_dict) > 0 else False
        _metadata_exif = _metadata[METADATA_EXIF]
        _image_geo_info = _metadata[IMAGE_GEO_INFO]

        # get fixed data and default values
        _offset_secs = 0
        try:
            _offset_secs = int(_offset.get(OFFSET_SECS, 0))
        except (ValueError, IndexError):
            pass
        # osm metadata
        _metadata_osm = _metadata[METADATA_OSM]

        _has_osm_latlon = False if len(_metadata_osm) == 0 else True
        _osm_latlon = _metadata_osm.get(LAT_LON)
        _osm_geo_info = _metadata_osm.get("geo_info")
        # _timezone = _metadata_osm.get("timezone", "Europe/Berlin")
        _gpx_sorter = None

        printt(f"### Collecting Image Metadata in path {C_F}[{str(_path)}]")
        if _has_osm_latlon:
            print(f"{C_H}    🎯 OSM Fallback: {_osm_latlon}, {_osm_geo_info}{C_0}")
        if _has_gps_track:
            print(f"{C_H}    🌍 GPS TRACK has [{len(_track_dict)}] trackpoints{C_0}")
            # now get the gps track into a sorted dict
            _gpx_sorter = BinarySorter(_track_dict, "utc_timestamp")

        # create the osm geo fallback information
        img_geo_osm_meta = None
        img_geo_osm_lat_lon = "not set"
        f_osm = "no_file"
        if _has_osm_latlon:
            img_geo_osm_meta = deepcopy(GEOTRACK_INFO)
            img_geo_osm_meta["geotrack_origin"] = GEOTRACK_ORIGIN_OSM
            img_geo_osm_meta["metadata_geo"] = _metadata_osm
            img_geo_osm_lat_lon = str(_metadata_osm[LAT_LON])
            f_osm = Path(_metadata_osm["file"]).name

        # now get all gps corrdinates
        printt(f"### Processing Images {C_F}[{str(_path)}]")
        for _f_img, _img_meta in _metadata_exif.items():
            img_geo: Dict = None

            # get geo data dict from GPX Track
            if _has_gps_track:
                img_geo = ImageOrganizer.get_img_geo_from_track(
                    metadata_exif=_img_meta, gpx_sorter=_gpx_sorter, time_offset_secs=_offset_secs
                )

            # as fallback use osm geodata if present
            if img_geo is None and _has_osm_latlon:
                print(f"{C_W}🌏 Using OSM Coordinates {C_F}[{f_osm}]: {C_S}{img_geo_osm_lat_lon}{C_0}")
                img_geo = deepcopy(img_geo_osm_meta)

            if img_geo is None:
                continue

            _image_geo_info[_f_img] = img_geo

        return _metadata

    def get_image_datetime_from_exif(self, exif_metadata_image: dict) -> Optional[DateTime]:
        """extracts date time from single image exif meta"""
        # get date of creation
        # try to get it from SubSecCreateDate
        #  "SubSecCreateDate": "2025:08:31 16:08:29.87+02:00",
        timezone_ = self._timezone
        datetime_format: str = "%Y:%m:%d %H:%M:%S.%f"
        datetime_s: Optional[str] = exif_metadata_image.get("Composite", {}).get("SubSecCreateDate")
        datetime_image: Optional[DateTime] = None

        # 1st fall back get it from EXIF
        if datetime_s is None:
            datetime_format = "%Y:%m:%d %H:%M:%S"
            datetime_s = exif_metadata_image.get("EXIF", {}).get("DateTimeOriginal")

        # 2nd fall back get it from File metadata
        if datetime_s is None:
            datetime_s = exif_metadata_image.get("File", {}).get("FileModifyDate")

        if datetime_s is not None:
            datetime_image = Helper.get_datetime_from_format_string(datetime_s, datetime_format, timezone_)
            return datetime_image

        return None

    def _collect_metadata_by_image(self) -> Optional[dict]:
        """gets all available metadata by file based on merged metadata.json"""
        if self._metadata is None:
            printe("No Metadata available, did you run merge_metadata ?")
            return
        metadata_exif: dict = self._metadata.get(METADATA_EXIF, {})
        # reverse geo from exiftool
        image_geo_info: dict = self._metadata.get(IMAGE_GEO_INFO, {})
        # reverse geo from web service
        image_reverse_geo_info: dict = self._metadata.get(IMAGE_REVERSE_GEO_INFO, {})

        # also try to get the gps track entry if existent
        gps_track: Optional[dict] = self._metadata.get(GPS_TRACK, {}).get(TRACK)
        num_gps = len(gps_track) if isinstance(gps_track, dict) else 0
        printd(f"[ImageOrganizer] Number of GPS Entries {C_F}[{num_gps}]")

        out = {}
        for filename, exifmeta in metadata_exif.items():
            _image_geo_info = image_geo_info.get(filename)
            _image_reverse_geo_info = image_reverse_geo_info.get(filename)

            out[filename] = {
                FILENAME: filename,
                FILEPATH: exifmeta.get("SourceFile"),
                DATETIME: self.get_image_datetime_from_exif(exifmeta),
                METADATA_EXIF: exifmeta,
                IMAGE_GEO_INFO: _image_geo_info,
                IMAGE_REVERSE_GEO_INFO: _image_reverse_geo_info,
                GPS_TRACK: None,
            }

            # get the gps track data entry from the metadata dictionary
            if gps_track is not None:
                timestamp: Optional[int] = None
                # try to get timestamp from reverse geo
                if isinstance(_image_reverse_geo_info, dict):
                    timestamp = _image_reverse_geo_info.get("extra", {}).get("timestamp_utc")
                # try to get from exiftool reverse geo api
                elif isinstance(_image_geo_info, dict):
                    timestamp = _image_geo_info.get("gps_info", {}).get("timestamp_gps")
                if timestamp is not None:
                    out[filename][GPS_TRACK] = gps_track.get(str(timestamp))
        return out

    def _prepare_exiftool_import(self) -> List[Dict]:
        """Based on previous actions, prepare a json file that can be used
        for changing EXIF Metadata using Exiftool"""
        out = []
        # _f_exiftool_import = self._f_exiftool_import
        _images_metadata = self._collect_metadata_by_image()
        _num_images = len(_images_metadata)
        print(f"{C_H}📷 [ImageOrganizer] Prepare Metadata Mapping for [{_num_images}] Images{C_0}")
        for _idx, (_filename, _img_metadata) in enumerate(_images_metadata.items()):
            Helper.show_progress(_idx, _num_images, "Mapped Images")
            _filename: str = _img_metadata.get(FILENAME)
            _file_path: str = _img_metadata.get(FILEPATH)
            _datetime_created: Optional[DateTime] = _img_metadata.get(DATETIME)
            _meta_dict: Optional[dict] = _img_metadata.get(METADATA_EXIF)
            _gps_track: Optional[dict] = _img_metadata.get(GPS_TRACK)

            # _gps_track: dict = _img_metadata.get(GPS_TRACK)
            _image_geo_info: dict = _img_metadata.get(IMAGE_GEO_INFO)
            _image_reverse_geo_info = _img_metadata.get(IMAGE_REVERSE_GEO_INFO)

            # TODO 🟡 SET DEFAULT KEYWORDS
            _keywords: Optional[list[str]] = None
            # TODO 🟡 SET THIS PARAMETER FROM ARGPARSE
            _map_exif2keywords: bool = True

            print_json(_meta_dict, f"Meta Dict for {C_F}[{_filename}]", True, "DEBUG")

            _transformer = GeoMetaTransformer(
                _filename,
                _meta_dict,
                _image_geo_info,
                _image_reverse_geo_info,
                _gps_track,
                _file_path,
                _datetime_created,
                _keywords,
                _map_exif2keywords,
            )
            _metadata_transformed = _transformer.transform()
            # geo metadata entry if found
            print_json(_gps_track, f"[ImageOrganizer] GPS GeoTrack Data for File {C_F}[{_filename}]", True, "DEBUG")
            # get the IPTC representation of the metadata / update the metadata file / it consists of cleaned IPTC DATA
            _metadata_iptc = GeoMetaTransformer.get_iptc_metadata(_metadata_transformed)
            # clean out any metadata not part of IPTC Metadata
            print_json(_metadata_iptc, f"[ImageOrganizer] IPTC Metadata for File {C_F}[{_filename}]", True, "DEBUG")
            _img_metadata[METADATA_EXIF][IPTC] = _metadata_iptc
            # now collect all keywords
            # TODO 🔵 add keyword update mode: replace, update
            _field_mapper = ExifToolFieldsMapper(_img_metadata[METADATA_EXIF], _metadata_transformed)
            _keywords = _field_mapper.get_keywords()

            print_json({"keywords": _keywords}, f"[ImageOrganizer] Keywords for File {C_F}[{_filename}]", True, "DEBUG")
            # Pull Together all metadata
            _metadata_transformed.update(_metadata_iptc)
            _metadata_transformed["keywords"] = _keywords
            # map the metadata as output
            _metadata_transformed = _field_mapper.map_metadata(_metadata_transformed)
            if len(_metadata_transformed) > 0:
                out.append(_metadata_transformed)

        return out

    def _merge_metadata(self) -> Dict:
        """Reads all metadata and writes them to a merged JSON.
        General Idea: Read available evn files from FILES_ENV
        and transfer the data to FILES or other segments of the file,
        if present
        """
        if self._prepare_exif_metadata is False:
            printd("Skip Preparation Step / Merging of Metadata")
            return

        _path = self._path
        printt(f"\n### Merge Image Metadata in {C_F}[{_path}]")

        config_metadata = deepcopy(CONFIG_METADATA)

        timestamp = DateTime.now()
        timestamp_utc = int(timestamp.replace(tzinfo=timezone.utc).timestamp())
        config_metadata[DATETIME] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        config_metadata[TIMESTAMP_UTC] = timestamp_utc
        files_env = config_metadata[FILES_ENV]
        files = config_metadata[FILES]
        files[CONFIG_F_METADATA] = os.path.join(_path, F_METADATA)
        offset = config_metadata[OFFSET]
        metadata_exif = config_metadata[METADATA_EXIF]

        # mapping the env file contents as refs to the values if these files are present
        env_fileref_map = {
            files_env[CONFIG_F_METADATA_ENV]: CONFIG_F_METADATA,
            files_env[CONFIG_F_METADATA_EXIF_ENV]: CONFIG_F_METADATA_EXIF,
            files_env[CONFIG_F_TIMESTAMP_IMG_ENV]: CONFIG_F_TIMESTAMP_IMG,
            files_env[CONFIG_F_OSM_ENV]: CONFIG_F_OSM,
            files_env[CONFIG_F_GPX_MERGED_ENV]: CONFIG_F_GPX_MERGED,
        }

        # copying the file names if they are present (without indirection / hardcoded names)
        env_file_map = {
            files_env[CONFIG_F_TIMESTAMP_CAMERA_ENV]: CONFIG_F_TIMESTAMP_CAMERA,
            files_env[CONFIG_F_TIMESTAMP_GPS_ENV]: CONFIG_F_TIMESTAMP_GPS,
            files_env[CONFIG_F_METADATA_GEO_REVERSE_ENV]: CONFIG_F_METADATA_GEO_REVERSE,
            files_env[CONFIG_F_EXIFTOOL_IMPORT_ENV]: CONFIG_F_EXIFTOOL_IMPORT,
        }

        # mapping the values in the env files to fields
        env_file_value_map = {
            files_env[CONFIG_F_OFFSET_ENV]: CONFIG_OFFSET_STR,
            files_env[CONFIG_F_OFFSET_SECS_ENV]: CONFIG_OFFSET_SECS,
        }

        # create the file references
        for env_ref, file_ref in env_fileref_map.items():
            f_env = _path.joinpath(env_ref)
            # print(f_env)
            if not f_env.is_file():
                printw(f"Refered reference {C_H}[{env_ref}] {C_F}[{f_env}] is not a file")
                continue
            env_file_ref = None
            try:
                env_file_ref = Persistence.read_txt_file(f_env)[0].strip()
            except (IndexError, KeyError):
                printe("No valid fileref found / empty file {C_F}[{f_env}]")
                continue
            if not os.path.isfile(env_file_ref):
                continue
            # assign value to target
            printh(f"Assigned [{file_ref}]: {C_F}[{env_file_ref}]")
            files[file_ref] = os.path.abspath(env_file_ref)

        # create the file refs for files with hardcoded names
        for env_ref, file_ref in env_file_map.items():
            f_env = _path.joinpath(env_ref)
            if not f_env.is_file():
                continue
            files[file_ref] = f_env
            printh(f"Assigned [{file_ref}]: {C_F}[{f_env}]")

        # reeading values
        # create the file references
        for env_ref, file_ref in env_file_value_map.items():
            f_env = _path.joinpath(env_ref)
            # print(f_env)
            if not f_env.is_file():
                continue

            value = None
            try:
                value = Persistence.read_txt_file(f_env)[0].strip()
            except (IndexError, KeyError):
                printe("Couldn't read file ref {C_F}[{f_env}]")
                continue
            if value is None:
                continue
            printh(f"Assigning [{file_ref}] from [{env_ref}]: {C_F}[{value}]")
            offset[file_ref] = value

        # now directly copy contents
        # copy the gpx merged json
        f_gpx_json: Path = None
        if files[CONFIG_F_GPX_MERGED]:
            f_gpx = Path(files[CONFIG_F_GPX_MERGED])
            f_gpx_json = f_gpx.parent.joinpath(f_gpx.stem + ".json")
        if f_gpx_json and f_gpx_json.is_file():
            files[CONFIG_F_GPX_MERGED_JSON] = str(f_gpx_json)

        # transform metadata_exif transforming it into a dict
        metadata_exif_dict = {}
        if files[CONFIG_F_METADATA_EXIF]:
            f_metadata_exif = Path(files[CONFIG_F_METADATA_EXIF])
            metadata_exif_list = Persistence.read_json(f_metadata_exif)
            for metadata_exif in metadata_exif_list:
                key = metadata_exif["File"]["FileName"]
                metadata_exif_dict[key] = metadata_exif

        config_metadata[METADATA_EXIF] = metadata_exif_dict

        # get the other json data
        maps_json = [
            {"file": CONFIG_F_TIMESTAMP_CAMERA, "dict": offset, "target": CONFIG_TIMESTAMP_CAMERA},
            {"file": CONFIG_F_TIMESTAMP_GPS, "dict": offset, "target": CONFIG_TIMESTAMP_GPS},
            {"file": CONFIG_F_OSM, "dict": config_metadata, "target": METADATA_OSM},
            {"file": CONFIG_F_GPX_MERGED_JSON, "dict": config_metadata, "target": GPS_TRACK},
        ]
        for map_json in maps_json:
            file_ref = files[map_json["file"]]
            if file_ref is None:
                continue
            map_json["dict"][map_json["target"]] = Persistence.read_json(file_ref)

        self._metadata = config_metadata
        return config_metadata

    @staticmethod
    def generate_timestamp_dict(
        source: Union[str, DateTime], filepath: Optional[Path] = None, datetime_only: bool = False
    ) -> Union[Dict[str, Any], Optional[DateTime]]:
        """
        Generate a standardized timestamp dictionary from a string or datetime object.

        Args:
            source (Union[str, DateTime]): Raw timestamp string or datetime object.
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
        if datetime_only:
            output = output["datetime"]

        return output

    # TODO CHECK
    # @staticmethod
    # def read_geosync_from_env(p_source: Path) -> str:
    #     """reads the offset string from the env file"""

    #     # get the geosync offset (previously written), with a default of 00:00:00
    #     f_offset = p_source.joinpath(F_OFFSET_ENV)
    #     lines = Persistence.read_txt_file(f_offset)
    #     t_offset = "+00:00:00" if len(lines) == 0 else lines[0]
    #     return f"-geosync={t_offset}"

    #  cmd = self._exiftool.cmd_export_meta()
    # def get_exiftool_cmd_export_meta(self, recursive: bool = False) -> list:
    #     """creates the exiftool command to export image data as json"""

    #     # command to export all exifdata in groups as json for given suffixes
    #     # progress is shown every 50 images
    #     # the c command is to format gps coordinates as decimals
    #     exiftool_cmd = CMD_EXIFTOOL_EXPORT_METADATA_RECURSIVE if recursive else CMD_EXIFTOOL_EXPORT_METADATA
    #     exif_cmd = exiftool_cmd.copy()
    #     exif_cmd.append(str(self._path))
    #     return exif_cmd

    # def get_exiftool_create_gps_metadata_from_gpx(self) -> list:
    #     """creates the exiftool command to create gpx data in image files

    #     Returns:
    #     bool: True if the command succeeded, False otherwise.
    #     """

    #     # use current path or input path
    #     p_work = self._path
    #     f_gpx_merged = p_work.joinpath(F_GPX_MERGED)

    #     f_gpx_merged = f_gpx_merged if f_gpx_merged.is_file() else None
    #     if f_gpx_merged is None:
    #         printh(f"No gpx file {f_gpx_merged} found, skip processing of creating gps based on gpx")
    #         return

    #     # get the geosync offset (previously written), with a default of 00:00:00
    #     geosync = self._exiftool.read_geosync_from_env()

    #     # command to geotag all elements in folder using an offset
    #     exif_cmd = CMD_EXIFTOOL_GEOTAG.copy()
    #     additional_params = [geosync, "-geotag", f_gpx_merged, str(p_source)]
    #     exif_cmd.extend(additional_params)
    #     # exif_cmd.append(additional_params)
    #     output = CmdRunner.run_cmd_and_print(exif_cmd)
    #     return output

    def _prepare_exif_metadata(self) -> None:
        """extract image metadata."""
        # All Metadata => metadata_exif.json
        # Exporting all metadata in a path into a json f_metadata_exif (metadata_exif.json)
        # runs: exiftool -r -g -c %.6f -progress 50 -json -<extensions> ...

        cmd_export_metadata = self._exiftool.cmd_export_meta()
        printh(f"    Create Metadata: {C_PY}[{cmd_export_metadata}]")
        f_metadata_exif_ = self._path.joinpath(self._f_metadata_exif)
        exif_metadata_created = CmdRunner.run_cmd_and_stream(cmd_export_metadata, f_metadata_exif_)
        if exif_metadata_created:
            Persistence.save_txt(self._path / F_METADATA_EXIF_ENV, str(f_metadata_exif_))

    def _prepare_track_metadata(self) -> None:
        """extract gps meta data."""
        f_gpx_merged_ = self._f_gpx_merged

        # 1. Create Merged GPS, if not already present: all gpx files => gpx_merged.gpx
        f_gpx = GeoLocation.merge_gpx(self._path, self._f_gpx_merged)
        gpx_file_created = False if f_gpx is None else True
        if gpx_file_created:
            printh(f"Merged GPX : {C_F}[{f_gpx}]")
            # store the file name of the merged gpx into an env file
            Persistence.save_txt(self._path.joinpath(F_GPX_MERGED_ENV), str(self._path.joinpath(f_gpx_merged_)))

        # 2. Select Reference File and extract timestanp of camera: = => timestamp_img.env
        timstamp_dict_camera: Dict = self.extract_image_timestamp()
        timestamp_camera_extracted = True if len(timstamp_dict_camera) > 0 else False
        if timestamp_camera_extracted:
            printh(f"Image timestamp: {C_PY}[{timstamp_dict_camera.get('original', 'NA')}]")

        # 3. Now Get the GPS Timestamp (as seen on the image of the previous image)
        #    Writes: offset.env, offset_sec.env, timestamp_gps.json, timestamp_camera.json
        time_offset = self.calculate_time_offset()
        printh(f"Image Offset: {C_PY}[{time_offset}]")

        # 4. Extract the OSM Link as default GPS Coordinates
        #   writes an existing of the existing openstreetmap.org links => osm.json,
        f_osm_info = F_OSM
        lat_lon = GeoLocation.get_openstreetmap_coordinates_from_folder(f_osm_info, self._path)
        lat_lon_extracted = False if lat_lon is None else True
        if lat_lon_extracted:
            printh(f"    LatLon from OSM: {C_PY}[{str(lat_lon)}]")
            Persistence.save_txt(self._path.joinpath(F_OSM_ENV), str(self._path.joinpath(f_osm_info)))

    def _prepare_exiftool_metadata(self) -> None:
        """parse the existing data into a plain json
        containing all metadata changes  by EXIFTOOL"""

        if self._action_prepare_transform is False:
            printd("[ImageOrganizer] transforming metadata to exiftool json file will be skipped")
            return

        # 9. Prepare exiftool json for import of Exiftool
        _exiftool_metadata = self._prepare_exiftool_import()
        if len(_exiftool_metadata) > 0:
            # TODO 🔵 make the import filename variable
            f_exiftool_metadata = self._path / F_EXIFTOOL_IMPORT
            self._metadata[FILES][CONFIG_F_EXIFTOOL_IMPORT] = str(f_exiftool_metadata)
            # also store the metadata in its own segment
            self._metadata[METADATA_EXIFTOOL] = _exiftool_metadata
            Persistence.save_json(f_exiftool_metadata, _exiftool_metadata)

    def prepare_collateral_files(self) -> None:
        """Prepare collateral files centrally.
        - Delete Collateral Files first
        - prepare collateral files
        - Merge GPX Files if there are any => F_GPX_ENV
        - Read Calibration Image  => F_TIMESTAMP_CAMERA
        - Read / Input GPS Time from Image => F_TIMESTAMP_GPS
        - Calculate Time Offset: F_TIMESTAMP_CAMERA / F_TIMESTAMP_GPS => F_OFFSET_ENV
        - Extract lat lon default from OSM links => F_LAT_LON_ENV
        """

        if self._action_prepare_meta is False:
            printd("[ImageOrganizer] prepare step will be skipped")
            return

        printt("### ImageOrganizer: prepare_collateral_files")
        #   creation of files per step
        # - [1] 🔢 metadata_exif.json
        # - [2] 🌍 gpx_merged.gpx
        # - [2] 🌍 osm.json
        # - [2] ⌚ timestamp_gps.json
        # - [2] ⌚ timestamp_camera.json
        # - [2] ⌚ offset.env
        # - [2] ⌚ offset_sec.env
        # - [2] ⌚ timestamp_img.env
        # - [6] 💾 exiftool_import.json
        # - [7] 🔢 metadata.json

        # 0. Delete any temporary files to start with a clean state
        self.cleanup_env_files(delete_generated_files=True)

        # 1. All Metadata => metadata_exif.json
        self._prepare_exif_metadata()

        # 2. Process GPS Track data => gpx_merged.gpx, timestamp_img.env
        #    offset.env, offset_sec.env, timestamp_gps.json,
        #    timestamp_camera.json, osm.json
        self._prepare_track_metadata()

        # 3. create a dict with all geo info metadata from osm link
        # - will be either created from reverse geo or from exiftool geolocation API
        # Will populate segments and refer single files
        # f_metadata,f_metadata_exif,f_timestamp_img,f_osm
        # f_gpx_merged,f_timestamp_camera,f_timestamp_gps
        # f_metadata_geo_reverse,f_exiftool_import
        # dict of merged meta data is returned / it's also in self._metadata
        _ = self._merge_metadata()

        # 4. Get the GPS metadata and add it to the merged file
        # if already saved
        # - use the collected exif data as input list
        # - amend the metadata.
        # - get latlon from track or from osm fallback
        # - augment metadata with found metadata
        gps_metadata = self._process_geo_metadata()

        gps_metadata_extracted = False if gps_metadata is None else True
        if gps_metadata_extracted:
            printh("    🌍 Processed GPS Metadata")

        # 5. use_reverse_geo if activated / returns the metadata
        # save geo reverse data (retrieved from external service as separate json)
        # returns the updated self._metadata
        _ = self.process_reverse_geo_metadata(overwrite=self._overwrite_reverse_geo)

        # 6. Create to EXIFTOOL JSON (exiftool_import.json)
        # that contains the metadata to be used as image metadata
        self._prepare_exiftool_metadata()

        # 7. Save all Data containing previous changes to a big metadata.json
        f_metadata = self._metadata[FILES][CONFIG_F_METADATA]
        Persistence.save_json(f_metadata, self._metadata)

    def extract_image_timestamp(self) -> Dict[str, Any]:
        """
        Extract SubSecDateTimeOriginal from an image using exiftool and return timestamp info.

        Args:
            filepath (Union[str, Path]): Path to the image file. If empty, fallback logic is applied.

        Returns:
            Dict[str, Any]: Dictionary with keys:
                - "original": original timestamp string from EXIF
                - "utc": UTC timestamp string
                - "timestamp": UTC timestamp in milliseconds
                - "datetime": datetime.date object
                - "filename": absolute path to the image file
        """
        # check for input and resaolve paths or files
        f = None
        p: Path = self._path
        # now determine file path
        if f is None:
            f = p / F_TIMESTAMP_IMG_DEFAULT
            # fallback no default gps image found ask user to enter
            if not f.exists():
                # note: is case sensitive
                jpg_files = list(p.glob("*.jpg"))
                if not jpg_files:
                    printe("No JPG files found in current directory.")
                    return {}
                printt("Select an image file to extract timestamp:")
                for idx, file in enumerate(jpg_files):
                    print(f"{C_I}[{idx}] {C_P}{file.name}{C_0}")
                try:
                    choice = int(inputc("Enter number of file to use").strip())
                    f = jpg_files[choice]
                except (ValueError, IndexError):
                    printe("Invalid selection.")
                    return {}

        if not f.exists():
            printe("File not found: {self._path}")
            return {}

        # save the timestamp image file to an env file
        Persistence.save_txt(p / F_TIMESTAMP_IMG_ENV, str(f))

        # Step 2: Run exiftool extracting Original DateTime Original

        timestamp_camera = self._exiftool.get_original_datetime(f)

        if timestamp_camera is None:
            printi(f"No GPS timestamp info created in Path {C_F}{str(f)}")
            return {}

        # Step 3: Capture output manually (if needed, could be redirected or parsed differently)
        timestamp_camera = timestamp_camera.strip()
        output = ImageOrganizer.generate_timestamp_dict(timestamp_camera, f)
        f_timestamp_camera = f.parent / F_TIMESTAMP_CAMERA
        Persistence.save_json(f_timestamp_camera, output)
        printh(f"GPS timestamp saved to {C_P}{f_timestamp_camera}")
        return output

    @staticmethod
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

        printt("\nMini Timeline:")
        printpy("GPS 🟦{' ' * (gps_pos)}|{' ' * (cam_pos - gps_pos - 1)}🟥 Camera")
        printh(f"{''.join(timeline)}")
        print(f"{C_B}Offset: {offset_sec:.3f} seconds{C_0}\n")

    @staticmethod
    def show_image(f_image: Path) -> None:
        """opens the camera image for display"""
        # read the file path
        if not f_image.is_file():
            printe("Can't open file [{f_image}]")
            return
        p_cwd = Path.cwd()
        printt(f"\n### Opening File in default image program: {C_F}[{f_image}]")
        os.chdir(f_image.parent)
        # open the image in the default viewer
        # the cmd command doesn't work here
        os.system(f"start {f_image.name}")
        os.chdir(p_cwd)

    def cleanup_env_files(self, delete_generated_files: bool = False) -> None:
        """CleanUp all ENV files and optionally also clean up generated meta files"""
        # env files that can be deleted right away
        delete_files = [F_TIMESTAMP_IMG_ENV, F_OFFSET_ENV, F_OFFSET_SECS_ENV, F_OSM_ENV]
        # env files that contain references to generated files
        delete_files_with_ref = [F_GPX_MERGED_ENV, F_METADATA_EXIF_ENV, F_METADATA_ENV]

        # delete env files with no ref to opther files
        for f_name in delete_files:
            f_del = self._path.joinpath(f_name)
            if f_del.is_file():
                printpy(f"🚮 Deleting {C_F}[{f_del}]")
                f_del.unlink(missing_ok=True)

        # delete env files with no ref to opther files
        for f_name in delete_files_with_ref:
            f_env = self._path.joinpath(f_name)
            if not f_env.is_file():
                continue
            if delete_generated_files:
                try:
                    f_del = Persistence.read_txt_file(f_env)[0].strip()
                    if os.path.isfile(f_del):
                        printpy(f"🚮 Deleting Generated {C_F}[{f_del}]")
                        os.remove(f_del)
                except IndexError:
                    pass
            printpy(f"🚮 Deleting {C_F}[{f_env}]")
            # f_env.unlink(missing_ok=True)

    def calculate_time_offset(self) -> str:
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
        offset_file = self._path / F_OFFSET_ENV
        offset_file_sec = self._path / F_OFFSET_SECS_ENV
        gps_json_file = self._path / F_TIMESTAMP_GPS
        camera_json_file = self._path / F_TIMESTAMP_CAMERA

        # Step 1: Remove existing offset file
        if offset_file.exists():
            try:
                offset_file.unlink()
                printpy("Deleted existing {offset_file}")
            except Exception as e:
                printe(f"Failed to delete {offset_file}: {e}")

        # Step 2: Load or generate timestamps
        camera_data: dict = Persistence.read_json(camera_json_file) if camera_json_file.exists() else {}
        # recreate the datetime for the reference image
        if len(camera_data) > 0:
            timestamp_camera = float(camera_data.get("timestamp", 0)) / 1000
            datetime_camera = DateTime.fromtimestamp(timestamp_camera)
            camera_data["datetime"] = datetime_camera

        # read gps data if already saved
        gps_data = Persistence.read_json(gps_json_file) if gps_json_file.exists() else {}

        if gps_data:
            timestamp_gps = float(gps_data.get("timestamp", 0)) / 1000
            datetime_gps = DateTime.fromtimestamp(timestamp_gps)
            gps_data["datetime"] = datetime_gps

        if not camera_data:
            printe("Missing TIMESTAMP_CAMERA.json. Offset will be set to zero.")
            offset_sec = 0
            offset_str = "+00:00:00"
        else:
            # create the date from camera
            if not gps_data:
                printe("Missing TIMESTAMP_GPS.json. Please enter GPS time manually")
                f_image = Path(camera_data.get("filename", "NA"))
                if f_image.is_file and self._show_gps_image:
                    printh(f"Show Image [{f_image}]")
                    ImageOrganizer.show_image(f_image)

                time_str = inputc(
                    f"Enter GPS time [hh:mm:ss] (blank to skip) {C_I}[CAMERA {datetime_camera.strftime('%H:%M:%S')}]"
                ).strip()
                try:
                    parts = [int(p) for p in time_str.split(":")]
                    while len(parts) < 3:
                        parts.append(0)
                    hour, minute, second = parts[:3]
                    local_zone = ZoneInfo(self._timezone)

                    # use date from camera and rest from input
                    dt_local = DateTime(
                        datetime_camera.year,
                        datetime_camera.month,
                        datetime_camera.day,
                        hour,
                        minute,
                        second,
                        0,
                        tzinfo=local_zone,
                    )
                    tz_offset = Helper.get_utc_offset(dt_local)
                    # get the date foramt string including time zone
                    dt_local_str = dt_local.strftime("%Y:%m:%d %H:%M:%S") + ".00" + tz_offset[:-3]
                    gps_data = ImageOrganizer.generate_timestamp_dict(dt_local)
                    gps_data["original"] = dt_local_str  # preserve user input
                    gps_data["filename"] = camera_data["filename"]  # preserve user input

                except Exception as _:
                    printe("No GPS Time found, will copy camera timestamps")
                    # copy the camera data as offset data of gps
                    gps_data = camera_data.copy()
                    _ = 0

            gps_ts = gps_data.get("timestamp", 0)
            cam_ts = camera_data.get("timestamp", 0)
            offset_sec = int((cam_ts - gps_ts) / 1000)
            offset_str = Helper.format_seconds_offset(offset_sec)
            dt_gps_str = gps_data["datetime"].strftime("%H:%M:%S")

            dt_cam_str = camera_data["datetime"].strftime("%H:%M:%S")
            offset_str2 = f"{str(offset_str).zfill(2)}"
            if offset_sec >= 0:
                c_offset = f"{C_PY}"
                offset_str2 = f"{C_PY}{offset_str2}"
            else:
                c_offset = f"{C_E}🚨 "
                offset_str2 = f"{C_E}🚨 {offset_str2}"

            printt(f"### Camera Times and Offset: {C_H}T(GPS) + T(OFFSET) = T(CAMERA)")
            print(f"{C_W}📷 Camera Time: {camera_data.get('original', 'N/A')}{C_0}")
            print(f"{C_I}🛰️ GPS Time   : {gps_data.get('original', 'N/A')}{C_0}")
            print(f"{c_offset}⌚ Offset (s) : {offset_sec}sec / {offset_str2}{C_0}")
            printh(f"🛰️+⌚=📷      : {C_I}{dt_gps_str}{offset_str2}{C_T}={C_W}{dt_cam_str}{C_0}\n")

            # render_mini_timeline(gps_ts, cam_ts)

        # Step 4: Save all outputs

        Persistence.save_json(camera_json_file, camera_data)
        printh(f"\nSaved camera timestamp to {C_P}{camera_json_file}")

        Persistence.save_json(gps_json_file, gps_data)
        printh(f"Saved GPS timestamp to {C_P}{gps_json_file}")
        # saving the offset in seconds
        Persistence.save_txt(offset_file, offset_str)
        printh(f"Saved offset [{offset_str}] to {C_P}{offset_file}")
        Persistence.save_txt(offset_file_sec, str(offset_sec))
        printh(f"Saved offset sec [{offset_sec}] to {C_P}{offset_file_sec}")
        return offset_str

    @staticmethod
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
        f_gps_merged = p_source.joinpath(F_GPX_MERGED_ENV)
        if f_gps_merged.is_file():
            return f_gps_merged
        # 2. Merge Any GPX Files into the standard one
        f_gps_merged = GeoLocation.merge_gpx(p_input, F_GPX_MERGED)
        if f_gps_merged:
            f_gps_merged = Path(f_gps_merged)
        return f_gps_merged

    # TODO 🟡 Rweview and clenaup
    # @staticmethod
    # def exiftool_add_gpsmeta_from_gps(
    #     p_source: Path, f_gps_track: str | Path | None, show_gps_image: bool = True
    # ) -> None:
    #     """
    #     Execute exiftool to add GPS Coordinates from a GPX Track.
    #     """
    #     p_cwd = os.getcwd()
    #     f_track = ImageOrganizer.resolve_gps_track(p_source, f_gps_track)
    #     if f_track is None:
    #         return
    #     # run in project path
    #     os.chdir(str(p_source))
    #     image_organizer = ImageOrganizer(path=p_source, timezone_s=TIMEZONE_DEFAULT, show_gps_image=show_gps_image)
    #     # clean up existing tmp files, get timestamps to calculate offset, get osm coordinates
    #     image_organizer.prepare_collateral_files()

    #     # read the geosync offset

    #     geosync = ExifTool(p_source).read_geosync_from_env()
    #     printt(f"### Using GPS Track {C_F}[{f_track}] (Offset {geosync})")

    #     # exiftool -geosync=+00:00:00 -geotag track.gpx *.jpg
    #     os.chdir(p_cwd)

    # TODO 🟡 Rweview and clenaup
    # @staticmethod
    # def exiftool_create_metadata_recursive(p_source: Path, f_metadata_exif: str = F_METADATA_EXIF) -> None:
    #     """
    #     Execute exiftool to extract metadata from image files in the input folder recursively.

    #     Runs exiftool with options to generate JSON metadata including specified image extensions,
    #     and writes the output to 'F_METADATA_EXIF' inside the output root folder.

    #     Args:
    #         input_folder (Path): Folder path containing images to analyze.
    #         output_root (Path): Folder where F_METADATA_EXIF will be saved.

    #     Prints:
    #         Status messages and exiftool progress output.
    #     """

    #     output_path = p_source / f_metadata_exif
    #     # CMD_EXIFTOOL_EXPORT_METADATA = [CMD_EXIFTOOL, "-r", "-g", "-c", "'%.6f'", "-progress50", "-json"] + SUFFIX_ARGS
    #  cmd = self._exiftool.cmd_export_meta()
    #     cmd = ImageOrganizer.get_exiftool_cmd_export_meta(p_source)

    #     cmd_output = CmdRunner.run_cmd_and_stream(cmd, output_path)
    #     if cmd_output:
    #         print(f"{C_H}Metadata successfully saved  {C_P}{output_path}")
    #         Persistence.save_txt(p_source / F_METADATA_EXIF_ENV, output_path)
    #     else:
    #         printe("Exiftool failed for command [{p_source}{C_0}]")

    # @staticmethod
    # def get_unprocessed_files(
    #     p_source: Union[str, Path], f_out: Optional[Union[str, Path]] = None
    # ) -> Dict[str, List[str]]:
    #     """
    #     Identify image files in the folder that lack corresponding backup files.

    #     For each file with a suffix in IMAGE_SUFFIXES, check if a backup file
    #     with the same name and suffix "<suffix>_original" exists. If not, add
    #     the full path to the output dictionary under "files_unprocessed".

    #     Args:
    #         folder (Union[str, Path]): Path to the folder to scan.
    #         f_out (Optional[Union[str, Path]]): Optional path or filename to save the output dictionary.

    #     Returns:
    #         Dict[str, List[str]]: Dictionary with key "files_unprocessed" and list of unmatched file paths.

    #     PROMPT
    #     Now add a function get_unprocessed_files that does the following:
    #     - For a given path it reads all files with the given suffix <suffix> defined in IMAGE_SUFFIXES
    #     - Check if for such a file a backup file having the same name and the suffix <suffix>_original exists
    #     - if it doesn't exist, add the full path of this file to an output dict under the attribute "files_unprocessed"
    #     - as output return this dictionary
    #     - Add an input param f_out to the function: if it's None, do nothing. if it is a string or path, save this dictionary under
    #     the path given by f_out. if it's just a name and not an absolute path, then use the current directory as save path

    #     """
    #     p_source = Path(p_source).resolve()
    #     output_dict = {"files_unprocessed": []}

    #     for suffix in IMAGE_SUFFIXES:
    #         pattern = f"*.{suffix}"
    #         for file_path in p_source.glob(pattern):
    #             backup_name = file_path.stem + f".{suffix}_original"
    #             backup_path = p_source / backup_name
    #             if not backup_path.exists():
    #                 output_dict["files_unprocessed"].append(str(file_path))

    #     # Save output if f_out is provided
    #     if f_out:
    #         f_out_path = Path(f_out)
    #         if not f_out_path.is_absolute():
    #             f_out_path = Path.cwd() / f_out_path
    #         Persistence.save_json(f_out_path, output_dict)

    #     return output_dict

    # @staticmethod
    # def process_metadata_json(metadata_path: Path) -> Dict[str, dict]:
    #     """
    #     Process the metadata JSON file to build a dictionary keyed by last four digits of filenames.

    #     Extracts datetime from 'SubSecDateTimeOriginal', converts it to a datetime object,
    #     extracts date string in YYYYMMDD format, and organizes data for each image.

    #     Args:
    #         metadata_path (Path): Path to the metadata JSON file.

    #     Returns:
    #         Dict[str, dict]: Dictionary mapping 4-digit keys to metadata with keys:
    #                         'key', 'filename', 'datetime_created' (datetime object), and 'date' string.
    #     """
    #     raw_data = Persistence.read_json(metadata_path)
    #     output_dict = {}
    #     if len(raw_data) == 0:
    #         return {}

    #     for entry in raw_data:
    #         try:
    #             source_file = entry["SourceFile"]
    #             dt_str = entry["Composite"]["SubSecDateTimeOriginal"]
    #             # transform dashes since they seem to lead to date
    #             # interpolation erorrs
    #             # 2025-10-06T19:03:19.400000+02:00
    #             dt_str = dt_str.replace(":", "-", 2)
    #             dt_obj = date_parser.parse(dt_str)
    #             date_str = dt_obj.strftime("%Y%m%d")
    #             filename = Path(source_file).name
    #             key = filename[-8:-4]  # last 4 digits as key
    #             output_dict[key] = {"key": key, "filename": filename, "datetime_created": dt_obj, "date": date_str}
    #         except Exception:
    #             # Skip entries missing required fields or malformed
    #             print(f"Error trying to parse {entry}")
    #             continue
    #     return output_dict

    # @staticmethod
    # def update_metadata_recursive(p_root: Path, f_metadata_exif: str = F_METADATA_EXIF) -> None:
    #     """
    #     Run exiftool on all first-level subfolders of output_root to update metadata.json files.
    #     Skips the root folder itself.

    #     Args:
    #         output_root (Path): The root folder containing dated subfolders.
    #     """
    #     child_folders = [f for f in p_root.iterdir() if f.is_dir()]
    #     summary = []

    #     print(f"\n{C_T}### Updating metadata.json in {len(child_folders)} subfolders...")
    #     for folder in child_folders:
    #         metadata_path = folder / f_metadata_exif
    #         files = list(folder.glob("*.*"))
    #         file_count = len(files)

    #         print(f"\n{C_H}Running exiftool in: {C_P}{folder}")
    #         # CMD_EXIFTOOL_EXPORT_METADATA = [CMD_EXIFTOOL, "-r", "-g", "-c", "'%.6f'", "-progress50", "-json"] + SUFFIX_ARGS
    #  cmd = self._exiftool.cmd_export_meta()
    #         cmd = ImageOrganizer.get_exiftool_cmd_export_meta(folder)
    #         cmd_output = CmdRunner.run_cmd_and_stream(cmd, metadata_path)
    #         status = "✅ Success" if cmd_output else "❌ Failed"
    #         summary.append({"folder": folder.name, "file_count": file_count, "status": status})
    #         if "failed" in status.lower():
    #             continue
    #         # save the env file
    #         Persistence.save_txt(folder / F_METADATA_EXIF_ENV, metadata_path)

    #     print(f"\n{C_T}### Metadata Update Summary:")
    #     for idx, entry in enumerate(summary):
    #         print(
    #             f"{C_H}- {C_I}[{str(idx).zfill(2)}] {C_P}{entry['folder']}{C_H}: "
    #             f"{C_B}{entry['file_count']} files, {entry['status']}"
    #         )

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def validate_p_source(args: argparse.Namespace) -> Path | None:
        """validates input folder if required"""
        # Determine input folder
        p_source = args.p_source
        if p_source is None:
            inp = inputc("Enter input folder path (default current folder)").strip()
            if inp:
                p_source = Path(inp)
            else:
                p_source = Path.cwd()
        else:
            p_source = Path(p_source)

        if not p_source.exists() or not p_source.is_dir():
            printe("Input folder {p_source} not found or invalid.")
            return None

        return p_source

    @staticmethod
    def cmd_validate_p_output(args: argparse.Namespace) -> Path | None:
        """validates output folder if required"""
        # Determine input folder
        p_output = args.p_output
        if p_output is None:
            outp = inputc("Enter output folder path (default current folder)").strip()
            if outp:
                p_output = Path(outp)
            else:
                p_output = Path.cwd()
        else:
            p_output = Path(p_output)

        if not p_output.exists() or not p_output.is_dir():
            printe("Input folder {p_output} not found or invalid.")
            return None

        return p_output

    def update_image_metadata(self) -> bool:
        """Update image metadata using exiftool"""
        if self._action_change_metadata is False:
            printd("Updating image metadata using exiftool will be skipped")
            return False
        # exiftool encoding
        exiftool_ = self._create_exiftool(encoding="utf8", progress=1)

        if exiftool_ is None:
            return False

        # TODO 🔵 add additional parameter for update
        return exiftool_.update_image_metadata(self._f_exiftool_import, "jpg")

    @staticmethod
    def cleanup_image_folder(
        p_root: Optional[str | Path], execute: bool = False, prompt_input: bool = True, revert: bool = False
    ) -> Optional[bool]:
        """cleans up an image folder"""
        execute_ = execute
        p_root_ = Path(p_root).absolute()
        files_delete: list = []
        files_relocate: list = []
        create_paths: list[Path] = []
        for subpath, _, files in os.walk(p_root_):
            subpath_: Path = Path(subpath).absolute()
            # an undo version to reverse file in RAW and AUX back to parent folder
            if revert is True:
                if subpath_.name in ["10_RAW", "20_AUX"]:
                    files_relocate.extend([[subpath_.joinpath(f), subpath_.parent] for f in files])
                continue
            else:
                if subpath_ != p_root_:
                    continue
            subpath_raw = subpath_.joinpath("10_RAW").absolute()
            subpath_aux = subpath_.joinpath("20_AUX").absolute()

            for f in files:
                f_: Path = subpath_.joinpath(f)
                if len(f_.suffix) > 0 and f_.suffix[1:] in FILESUFFIX_DO_NOT_MOVE:
                    continue
                elif f.lower() in FILES_DO_NOT_MOVE:
                    continue
                elif f.lower() in FILES_DELETE:
                    files_delete.append(f_)
                    continue
                suffix = "unknown" if len(f_.suffix) == 0 else (f_.suffix[1:]).lower()
                if suffix in FILETYPE_IMG:
                    continue
                elif suffix in FILETYPE_TMP:
                    files_delete.append(f_)
                elif suffix in FILETYPE_RAW:
                    files_relocate.append([f_, subpath_raw])
                    if subpath_raw not in create_paths:
                        create_paths.append(subpath_raw)
                else:
                    files_relocate.append([f_, subpath_aux])
                    if subpath_aux not in create_paths:
                        create_paths.append(subpath_aux)

        printt(f"\n### Cleanup Folder {C_F}[{str(p_root)}")
        printt(f"    ♻️ Delete {C_PY}[{len(files_delete)}]")
        for f in files_delete:
            printd(f"    *  {str(f)}")
        printt(f"    ➡️ Move   {C_PY}[{len(files_relocate)}]")
        for f in files_relocate:
            printd(f"    *  {str(f[0])}")

        if (len(files_delete) + len(files_relocate)) == 0:
            printi(f"Nothing to clean up in folder {C_F}[{str(p_root)}]")
            return

        if prompt_input and execute:
            execute_ = True if str(inputc("Comtinue with folder cleanup (y)").lower()) == "y" else False

        if execute_ is False:
            return

        # create subfolders
        for _p in create_paths:
            _p.mkdir(parents=True, exist_ok=True)

        for f in files_delete:
            Persistence.relocate_file(f, action="delete")

        for f in files_relocate:
            Persistence.relocate_file(f_src=f[0], f_trg=f[1], action="move")

        return True

    @staticmethod
    def rename_images(
        p_root: Union[str, Path], execute: bool = True, prompt_input: bool = True
    ) -> Optional[List[tuple]]:
        """Rename Raw and unnamed Images according to the lowermost path as prefix
        returns old name / new name as tuple
        """
        execute_ = execute
        out = []
        regex_date_pattern = re.compile(r"\d{8}")  # exactly 8 digits
        # matching exactly 8 digits (date) at the start
        regex_date_pattern = re.compile("^(?<!\d)\d{8}(?!\d)")
        # regex for 4 digits (image index number)
        regex_image_index_pattern = re.compile("(?<!\d)\d{4}(?!\d)")

        def extract_lowermost_date_path(path: str) -> Optional[str]:
            """gets the deepest parent path matching 8 characters / path format"""
            p = Path(path)
            # only use the path part
            if p.is_file():
                p = p.parent

            # iterate from deepest parent upward
            for part in reversed(p.parts):
                if regex_date_pattern.search(part):
                    return part

            return None

        def get_image_number(path: str) -> Optional[str]:
            """extract the image number from a filename
            drop the first 4 characters and search in the rest of the filename
            """
            p = Path(path)
            if not p.is_file():
                return
            filename = p.stem
            if len(filename) <= 4:
                return
            filename = filename[4:]

            image_number = None
            try:
                image_number = regex_image_index_pattern.findall(filename)[-1]
            except IndexError:
                pass
            return image_number

        p_root_ = p_root

        file_list = Helper.get_file_dict(p_root_, as_list=True)
        if file_list is None:
            return

        num_files = len(file_list)

        # for each file, try to check whether there is an index (4digit number somewhere in the file
        # name and a valid path containing an 8 digit path somewhere
        _last_wrong_path = None
        _failed_files = []
        _failed_paths = []
        for idx, f in enumerate(file_list):
            file: Path = Path(f)
            _current_path = str(file.parent)
            date_path = extract_lowermost_date_path(f)
            if date_path is None and _current_path != _last_wrong_path:
                _last_wrong_path = _current_path
                printd(f"Couldn't find a parent path containing date in path [{_last_wrong_path}]")
                _failed_files.append(f)
                _failed_paths.append(_last_wrong_path)
                continue

            if _current_path == _last_wrong_path:
                _failed_files.append(f)
                continue

            image_number = get_image_number(f)
            if image_number is None:
                printd(f"No index number in file [{f}]")
                _failed_files.append(f)
                continue

            new_file_name: str = f"{date_path}_{image_number}{file.suffix}"
            # skip files that were renamed already
            if file.name == new_file_name:
                continue

            out.append([f, os.path.join(_current_path, new_file_name)])
            Helper.show_progress(
                idx,
                num_files,
                f"Extracting Image Numbers ✅{str(len(out)).zfill(3)} ❌{str(len(_failed_files)).zfill(3)})",
            )

        if len(out) == 0:
            printi(f"No files to rename in path {C_F}[{str(p_root)}]")
            return

        printt("### RENAME FILES")
        for f_old, f_new in out:
            print(f"{C_PY}* {str(f_old):<70}=> {C_S}{Path(f_new).name}")

        if len(out) == 0:
            printh(f"No files to rename, path {C_F}[{str(p_root)}]")

        if prompt_input and execute:
            execute_ = True if str(inputc("Continue with renaming files (y)").lower()) == "y" else False

        if execute_ is False:
            return

        num_files = len(out)
        for idx, (f_old, f_new) in enumerate(out):
            Helper.show_progress(idx, num_files)
            Persistence.relocate_file(f_old, f_new, action="rename")
        return out

    @staticmethod
    def run_image_actions_recursive(
        p_root: str,
        action: Literal["rename", "cleanup"] = "rename",
        execute: bool = False,
        prompt_input: bool = True,
        revert: bool = False,
    ) -> Optional[List[tuple]]:
        """run actions for first level folders"""
        p_root_ = Path(p_root).absolute()
        rename_images = []

        # functions to decode
        for subpath, _, _ in os.walk(p_root):
            subpath_ = Path(subpath).absolute()
            # only process direct children of root path
            if subpath_.parent != p_root_:
                continue

            if action == "rename":
                rename_images_ = ImageOrganizer.rename_images(subpath, execute, prompt_input)
                if isinstance(rename_images_, list):
                    rename_images.extend(rename_images_)
            elif action == "cleanup":
                ImageOrganizer.cleanup_image_folder(subpath, execute, prompt_input, revert)

        return rename_images

    @staticmethod
    def move_images(
        p_from: Optional[str],
        p_to: Optional[str],
        execute: bool = False,
        prompt_input: bool = True,
        f_exiftool: str = CMD_EXIFTOOL,
        encoding="latin",
        language: str = "de",
    ) -> List[tuple]:
        """bundles similar files in a source folder (recursively) and will move them to a Date Based subfolder residing in target folder"""
        execute_ = execute
        cwd_: Path = Path.cwd()
        p_from_: Path = cwd_ if p_from is None else Path(str(p_from))
        p_to_: Path = cwd_ if p_to is None else Path(str(p_to))
        if not p_from_.is_dir():
            printe(f"[Image Organizer] Source path [{p_from}] is invalid")
            return
        if not p_to_.is_dir():
            printe(f"[Image Organizer] Target path [{p_to}] is invalid")
            return

        file_list = Helper.get_file_dict(p_from, as_list=True)
        if file_list is None:
            printi(f"[Image Organizer] move_images: no files found in [{p_from}]")
            return

        exiftool_ = ExifTool(
            path=p_from, encoding=encoding, language=language, f_exiftool=f_exiftool, show_output=False
        )

        # collect files in a dict with keys [parent_path][stem][file(Path)]
        path_dict_: dict[str, dict[str, list[Path]]] = {}
        num_files_total: int = 0
        for f in file_list:
            file = Path(f).absolute()
            # TODO 🔵 also move to subpaths if original files are nested
            parent_path = str(file.parent)
            stem = file.stem
            # suffix = file.suffix[1:]
            # get the path dict
            stem_dict = path_dict_.get(parent_path)
            if stem_dict is None:
                stem_dict = {}
                path_dict_[parent_path] = stem_dict
            # collect files with same stems
            files_list = stem_dict.get(stem)
            if files_list is None:
                file_list = []
                stem_dict[stem] = file_list
            file_list.append(file)
            num_files_total += 1

        files_by_date_dict: dict[str, list] = {}
        files_not_matched: list = []
        num_files = 0
        for parent_path, stem_dict in path_dict_.items():
            Helper.show_progress(num_files_total, num_files, f"Preparing file move (Path [{parent_path}])")
            for stem, files in stem_dict.items():
                yyyymmdd: str = None
                # get the first image file occurence and extract the date
                for f in files:
                    if len(f.suffix) == 0 or ((f.suffix[1:]).lower() not in IMAGE_SUFFIXES):
                        continue
                    # try to get a date from the first valid occurence
                    timestamp_image: Optional[str] = exiftool_.get_original_datetime(f)
                    if timestamp_image is None:
                        continue
                    timestamp_image = timestamp_image.strip()
                    timestamp: DateTime = ImageOrganizer.generate_timestamp_dict(timestamp_image, datetime_only=True)
                    yyyymmdd = timestamp.strftime("%Y%m%d")
                    break
                num_files += len(files)
                if yyyymmdd is None:
                    files_not_matched.extend(files)
                    continue
                files_by_date = files_by_date_dict.get(yyyymmdd)
                if files_by_date is None:
                    files_by_date = []
                    files_by_date_dict[yyyymmdd] = files_by_date
                files_by_date.extend(files)

        move_files: list = []
        for date_s, files in files_by_date_dict.items():
            datetime_target_path = p_to_.joinpath(date_s)
            if execute_:
                datetime_target_path.mkdir(parents=False, exist_ok=True)

            printd(f"Moving [{str(len(files)).zfill(3)}] files to folder [{str(datetime_target_path)}]")

            for f in files:
                move_files.append((f, datetime_target_path))

        if len(move_files) == 0:
            printi(f"No files to move from {C_F}[{str(p_from)}]")
            return []

        if prompt_input and execute:
            execute_ = True if str(inputc("Comtinue with moving files (y)").lower()) == "y" else False

        if execute_ is False:
            return []

        for f_src, f_trg in move_files:
            Persistence.relocate_file(f_src, f_trg)
        return move_files

    @staticmethod
    def build_arg_parser() -> argparse.ArgumentParser:
        """
        Create and return a command-line argument parser for the program.

        The parser supports optional input folder and output root folder arguments,
        both defaulting to None to allow interactive prompts if not provided.

        Returns:
            argparse.ArgumentParser: Configured argument parser.
        """
        parser = argparse.ArgumentParser(description="Auto organize images by date using exif metadata.")

        # used in main / OK
        parser.add_argument(
            "--action_show_args",
            "--action-show-args",
            action="store_true",
            help="Show the arparse args when running the image organizer",
        )

        # used in main / OK
        parser.add_argument(
            "--action_move_images",
            "--action-move-images",
            action="store_true",
            help="Move Images from a source folder to a target folder",
        )

        # used in main / OK
        parser.add_argument(
            "--action_rename_images",
            "--action-rename-images",
            action="store_true",
            help="Rename Images according to foller containing date in path",
        )

        # used in main / OK
        parser.add_argument(
            "--action_cleanup_images",
            "--action-cleanup-images",
            "-clean",
            action="store_true",
            help="CleanUp Image Folder",
        )

        # used in main / OK
        parser.add_argument(
            "--action_cleanup_images_undo",
            "--action-cleanup-images-undo",
            "-revert",
            action="store_true",
            help="CleanUp Image Folder Undo (move images back)",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--action_prepare_meta",
            "--action-prepare-meta",
            "-prepare",
            action="store_true",
            help="Prepare collateral files for metadata update",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--action_prepare_transform",
            "--action-prepare-transform",
            "-transform",
            action="store_true",
            help="Transform image metadata to a json for EXIFTOOL metadata changes",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--action_change_metadata",
            "--action-change-metadata",
            "-change",
            action="store_true",
            help="Change image metadata using EXIFTOOL",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--p_source",
            "--p-source",
            "--p_from",
            "--p-from",
            "-from",
            "-src",
            type=str,
            default=None,
            help="Source folder path where images were dumped (default: current folder if empty)",
        )
        parser.add_argument(
            "--p_output",
            "--p-output",
            "--p_to",
            "--p-to",
            "--p_target",
            "--p-target",
            "-trg",
            "-to",
            "-out",
            type=str,
            default=None,
            help=f"Output root folder where date folders are created (default: {str(P_PHOTO_OUTPUT_ROOT)})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--print_level",
            "--print-level",
            type=str,
            default="INFO",
            help="Print Level (DEBUG,INFO,WARNING,ERROR), if not set as ENV MY_PRINT_LEVEL (Default: INFO)",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--timezone",
            "--timezone",
            "-tz",
            type=str,
            default=TIMEZONE_DEFAULT,
            help=f"Timezone (Default: {TIMEZONE_DEFAULT})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--max_timediff",
            "--max-timediff",
            type=int,
            default=300,
            help="Maximum Timedifference GPS vs Camera Timestamp (300)",
        )

        # can be utf-8, latin1, cp1252
        parser.add_argument(
            "--encoding",
            type=str,
            default="latin1",
            help="Character encoding for file names and image metadata (default: latin1)",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--do_not_show_gps_image",
            "--do-not-show-gps-image",
            "-noshow",
            action="store_true",
            help="Do not show a preview of the GPS file",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--do_not_use_reverse_geo",
            "--do-not-use-reverse-geo",
            action="store_true",
            help="Do not use reverse geo service",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--overwrite_reverse_geo",
            "--overwrite-reverse-geo",
            action="store_true",
            help="Overwrite the reverse geo info file",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--f_metadata",
            "--f-metadata",
            type=str,
            default=F_METADATA,
            help=f"Filename of Metadata File (Default: {F_METADATA})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--f_metadata_exif",
            "--f-metadata-exif",
            type=str,
            default=F_METADATA_EXIF,
            help=f"Filename of Metadata File Containing Exif Data Only (Default: {F_METADATA_EXIF})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--f_reverse_geo",
            "--f-reverse-geo",
            type=str,
            default=F_METADATA_GEO_REVERSE,
            help=f"Filename of Reverse Geo File (Default: {F_METADATA_GEO_REVERSE})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--f_gpx_merged",
            "--f-gpx-merged",
            type=str,
            default=F_GPX_MERGED,
            help=f"Filename of Merged GPX File (Default: {F_GPX_MERGED})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--f_exiftool_import",
            "--f-exiftool-import",
            type=str,
            default=F_EXIFTOOL_IMPORT,
            help=f"Filename cotnaining exiftool import data (Default: {F_EXIFTOOL_IMPORT})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--cmd_exiftool",
            "--cmd-exiftool",
            type=str,
            default=CMD_EXIFTOOL,
            help=f"Path to ExifTool Executable (Default:{CMD_EXIFTOOL})",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--language",
            type=str,
            default="de",
            help="Language Code (Used for ExifTool, default: de)",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--do_not_show_exiftool_output",
            "--do-not-show-exiftool-output",
            action="store_true",
            help="Hide Exiftool Output Info Messages",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--auto_confirm",
            "--auto_confirm",
            "-y",
            action="store_true",
            help="Auto Confirm User Input",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--dry_run",
            "--dry-run",
            action="store_true",
            help="Only Dry Run, Do Not Save",
        )

        # part of ImageOrganizer Constructor
        parser.add_argument(
            "--recursive",
            "-r",
            action="store_true",
            help="Process Subfolders to allow for bulk operations for cleanup and rename action",
        )

        # TODO 🟡 Allow to add keyword sets and to select them interactively or by default choice
        # TODO 🔵 Allow to add lens make from a file to select interactively or by default choice

        return parser

    @staticmethod
    def argparse_set_defaults(args: argparse.Namespace) -> argparse.Namespace:
        """Sets the argparse defaults if not already covered by defaults"""
        # source path
        if args.p_source is None:
            args.p_source = os.getcwd()
        if args.p_output is None:
            args.p_output = str(P_PHOTO_OUTPUT_ROOT)

        return args

    @classmethod
    def create_image_organizer(cls, args: argparse.Namespace) -> Optional[ImageOrganizer]:
        """create an image Organizer instance"""

        return cls(
            action_prepare_meta=args.action_prepare_meta,
            action_prepare_transform=args.action_prepare_transform,
            action_change_metadata=args.action_change_metadata,
            path=args.p_source,
            timezone_s=args.timezone,
            max_timediff=args.max_timediff,
            encoding=args.encoding,
            show_gps_image=(not args.do_not_show_gps_image),
            use_reverse_geo=(not args.do_not_use_reverse_geo),
            overwrite_reverse_geo=args.overwrite_reverse_geo,
            f_metadata=args.f_metadata,
            f_metadata_exif=args.f_metadata_exif,
            f_reverse_geo=args.f_reverse_geo,
            f_gpx_merged=args.f_gpx_merged,
            f_exiftool_import=args.f_exiftool_import,
            cmd_exiftool=args.cmd_exiftool,
            language=args.language,
            cmd_exiftool_output=(not args.do_not_show_exiftool_output),
            auto_confirm=args.auto_confirm,
        )


def main() -> None:
    """
    Main function that orchestrates reading arguments, running exiftool,
    processing metadata, moving files, updating metadata in date folders,
    and printing results.

    Interactively prompts for inputs if no arguments are specified.
    """

    # parse from commmand line
    parser = ImageOrganizer.build_arg_parser()
    args = parser.parse_args()
    # set defaults
    args = ImageOrganizer.argparse_set_defaults(args)
    prompt_: bool = not args.auto_confirm
    execute: bool = not args.dry_run
    recursive: bool = args.recursive
    revert_cleanup: bool = args.action_cleanup_images_undo
    if revert_cleanup:
        args.action_cleanup_images = True

    # set print level / default is info
    if os.environ.get("MY_PRINT_LEVEL") is None:
        set_print_level(args.print_level, show_emoji=True)

    if args.action_show_args:
        print_json(vars(args), "ARGPARSER SETTINGS")

    # move items from a dump folder into separate folders
    if args.action_move_images:
        _ = ImageOrganizer.move_images(
            p_from=args.p_source,
            p_to=args.p_output,
            execute=execute,
            prompt_input=prompt_,
            f_exiftool=args.cmd_exiftool,
            encoding=args.encoding,
            language=args.language,
        )
        return

    # rename or clean up everything in 1st level children folders
    if recursive:
        if args.action_rename_images:
            ImageOrganizer.run_image_actions_recursive(args.p_source, "rename", execute, prompt_)
            return
        elif args.action_cleanup_images:
            ImageOrganizer.run_image_actions_recursive(args.p_source, "cleanup", execute, prompt_, revert_cleanup)
            return
    # rename or clean up everything under a given folder
    else:
        if args.action_rename_images:
            ImageOrganizer.rename_images(args.p_source, execute, prompt_)
            return
        elif args.action_cleanup_images:
            ImageOrganizer.cleanup_image_folder(args.p_source, execute, prompt_, revert_cleanup)
            return

    # create the Image organizer
    image_organizer: ImageOrganizer = ImageOrganizer.create_image_organizer(args)

    # create all metadata
    image_organizer.prepare_collateral_files()

    # apply metadata changes
    image_organizer.update_image_metadata()


if __name__ == "__main__":
    main()
