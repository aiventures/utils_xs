"""Some Python Helper functions"""

import sys
import logging
import re

import argparse
import json
from json import JSONDecodeError


# import datetime
from datetime import timedelta
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
    def format_seconds_offset(offset_s: int) -> str:
        """Format offset as (+/-)HH:MM.SS String"""
        sign = "+" if offset_s >= 0 else "-"
        abs_seconds = abs(offset_s)
        hours, remainder = divmod(abs_seconds, 3600)
        minutes, offset_s = divmod(remainder, 60)
        return f"{sign}{hours:02}:{minutes:02}:{offset_s:02}"

    @staticmethod
    def get_datetime_from_format_string(
        dt_str: str,
        timezone="Europe/Berlin",
        time_format="%Y:%m:%d %H:%M:%S",
        offset_sec: int = 0,
    ) -> DateTime:
        """converts into datetime"""

        # Parse the string into a naive datetime object
        dt_naive = DateTime.strptime(dt_str, time_format)

        # Attach a time zone (e.g., Europe/Berlin)
        dt_local = dt_naive.replace(tzinfo=ZoneInfo(timezone))
        dt_local += timedelta(seconds=offset_sec)
        return dt_local

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
        dt = DateTime.now()
        if isinstance(dt_in, str):
            dt = Helper.get_datetime_from_format_string(dt_in, timezone, time_format, offset_sec)
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
    def run_cmd_and_stream(cmd: List[str], output_path: Path) -> list:
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
            with output_path.open("w", encoding="utf-8") as outfile:
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
    def run_cmd_and_print(cmd: List[str], decode: bool = True) -> list:
        """
        Run a command and print both stdout and stderr to the console in real time.

        Args:
            cmd (List[str]): The command to execute.

        Returns:
            bool: True if the command succeeded, False otherwise.
        """
        out = []
        print("hugo cmd ", cmd)

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Stream both stdout and stderr
            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if stdout_line:
                    _s = stdout_line.strip()
                    if decode:
                        _s = _s.encode("latin1").decode("utf-8")
                    out.append(_s)
                    print(f"{C_PY}[CMD] {_s}{C_0}")
                if stderr_line:
                    _s = stderr_line.strip()
                    if decode:
                        _s = _s.encode("latin1").decode("utf-8")
                    out.append(_s)
                    print(f"{C_E}[ERR] {_s}{C_0}")

                if not stdout_line and not stderr_line and process.poll() is not None:
                    break

            return out

        except Exception as e:
            print(f"{C_E}Failed to run command: {e}{C_0}")

        return out


class GeoLocation:
    """Helper for Geolocation Handling."""

    CMD_EXIFTOOL_REVERSE_GEO = [CMD_EXIFTOOL, "-g3", "-a", "-json", "-lang", "de", "-api"]

    @staticmethod
    def create_gpx_header(soup: BeautifulSoup) -> Tag:
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
    def merge_gpx(p_source: Union[str, Path], f_output: Union[str, Path]) -> Union[str, None]:
        """
        Merge multiple GPX files in a folder into a single GPX file.

        - Uses metadata from the file with the earliest <metadata><time>
        - Collects all <trkpt> segments and sorts them by <time>
        - Saves the merged GPX to f_output

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
            print(f"{C_T}File {C_F}[{f_output}]{C_T} already exists {C_0}")
            return

        gpx_files = sorted(p_source.glob("*.gpx"))
        if not gpx_files:
            print(f"{C_E}No GPX files found in {C_F}{p_source}{C_0}")
            return None

        metadata_time_map = {}
        trkpt_elements = []

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

        trkpt_elements.sort(key=trkpt_time)

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
        for trkpt in trkpt_elements:
            trkseg_tag.append(trkpt)
        trk_tag.append(trkseg_tag)
        gpx_tag.append(trk_tag)

        # Save to file
        soup_str = soup_out.prettify()
        Persistence.save_txt(f_output, soup_str)
        # with f_output.open("w", encoding="utf-8") as f:
        #     f.write(str(soup_out))

        print(f"{C_T}Merged GPX saved to {C_H}{f_output}{C_0}")
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
            print(f"{C_E}Invalid folder: {folder}{C_0}")
            return None

        env_file = folder / file
        if env_file.exists():
            try:
                env_file.unlink()
                print(f"{C_T}Deleted existing {env_file}{C_0}")
            except Exception as e:
                print(f"{C_E}Failed to delete {env_file}: {e}{C_0}")

        url_files = list(folder.glob("*.url"))
        output = {}

        for idx_f, f in enumerate(url_files, 1):
            output_per_file = {}
            output[idx_f] = output_per_file
            output_per_file["idx"] = idx_f
            output_per_file["file"] = f
            url = Persistence.read_internet_shortcut(str(f))
            if url and "openstreetmap.org" in url.lower():
                coords = GeoLocation.latlon_from_osm_url(url)
                output_per_file["lat_lon"] = coords
                output_per_file["geo_reverse"] = {}
                if coords:
                    # CMD_EXIFTOOL_REVERSE_GEO = [CMD_EXIFTOOL, "-g3", "-a", "-json", "-lang", "de", "-api", "geolocation"]
                    lat_lon = f"geolocation={coords[0]}, {coords[1]}"
                    cmd_exiftool_reverse = GeoLocation.CMD_EXIFTOOL_REVERSE_GEO.copy()
                    cmd_exiftool_reverse.append(lat_lon)
                    # get reverse geocoordinates
                    reverse_geo_s = "".join(CmdRunner.run_cmd_and_print(cmd_exiftool_reverse))
                    geo_reverse = {}
                    geo_info = "No Reverse Geo Info"
                    if reverse_geo_s:
                        try:
                            geo_reverse = json.loads(reverse_geo_s)[0]
                            # print(json.dumps(reverse_geo, indent=4))
                            geo_reverse = geo_reverse.get("Main", {})
                            output_per_file["geo_reverse"] = geo_reverse
                            city = geo_reverse.get("GeolocationCity")
                            region = geo_reverse.get("GeolocationRegion")
                            subregion = geo_reverse.get("GeolocationSubregion")
                            time_zone = geo_reverse.get("GeolocationTimeZone", "Europe/Berlin")
                            distance = geo_reverse.get("GeolocationDistance")
                            bearing = geo_reverse.get("GeolocationBearing")
                            geo_info = f"{distance}, {bearing}° to {city}/{subregion}/{region}"
                            output_per_file["geo_info"] = geo_info
                            output_per_file["time_zone"] = time_zone
                            print(
                                f"\n{C_T}### OSM Coordinates {C_F}[{f.name}]: {C_Q}{coords}, {C_H}{geo_info} ({time_zone}){C_0}"
                            )

                        except (JSONDecodeError, IndexError) as e:
                            print(
                                f"{C_E}Error occured during parsing OSM Coordinates [{coords}],reverse geo:[{reverse_geo_s}], {e}"
                            )
                            continue
                    # print(reverse_geo_s)
                    # output.append((f.name, coords, geo_info, geo_reverse))

        if not output:
            print(f"{C_W}No OpenStreetMap links with coordinates found in {folder}{C_0}")
            return None

        if len(output) == 1:
            selected = next(iter(output.values()))
            print(f"{C_T}Found one OpenStreetMap link: {C_P}{selected['file']}{C_0}")
        else:
            print(f"{C_T}Multiple OpenStreetMap links found:{C_0}")
            for idx, info in output.items():
                coords = info.get("lat_lon", ("NA", "NA"))
                geo_info = info.get("geo_info", "NA")
                print(
                    f"{C_I}[{idx}] {C_P}{f}{C_T} → lat: {coords[0]:.5f}, lon: {coords[1]:.5f}{C_0},info: {geo_info} {C_0}"
                )

            try:
                choice = int(input(f"{C_Q}Enter number of file to use: {C_0}").strip())
                selected = output[choice]
            except (ValueError, IndexError):
                print(f"{C_E}Invalid selection. No coordinates returned.{C_0}")
                return None

        try:
            Persistence.save_json(env_file, selected)
            print(f"{C_H}Saved Geo Info to {C_P}{env_file}{C_0}")
        except Exception as e:
            print(f"{C_E}Failed to write coordinates: {e}{C_0}")

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
            print(f"{C_E}Invalid folder: {folder}{C_0}")
            return None

        env_file = folder / file
        if env_file.exists():
            try:
                env_file.unlink()
                print(f"{C_T}Deleted existing {env_file}{C_0}")
            except Exception as e:
                print(f"{C_E}Failed to delete {env_file}: {e}{C_0}")

        gpx_files = list(folder.glob("*.gpx"))
        if not gpx_files:
            print(f"{C_E}No GPX files found in {folder}{C_0}")
            return None

        if len(gpx_files) == 1:
            selected = gpx_files[0].name
            try:
                env_file.write_text(selected + "\n", encoding="utf-8")
                print(f"{C_H}Saved GPX filename [{selected}] to {C_P}{env_file}{C_0}")
            except Exception as e:
                print(f"{C_E}Failed to write GPX filename: {e}{C_0}")
            return selected

        print(f"{C_T}Multiple GPX files found:{C_0}")
        for idx, f in enumerate(gpx_files):
            print(f"{C_I}[{idx}] {C_P}{f.name}{C_0}")

        try:
            choice = int(input(f"{C_Q}Enter number of file to use: {C_0}").strip())
            selected = gpx_files[choice].name
            env_file.write_text(selected + "\n", encoding="utf-8")
            print(f"{C_H}Saved GPX filename [{selected}] to {C_P}{env_file}{C_0}")
            return selected
        except (ValueError, IndexError):
            print(f"{C_E}Invalid selection. No GPX file saved.{C_0}")
            return


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
                    if line[0] == comment_marker:
                        continue
                    lines.append(line.strip())
        except:
            logger.error(f"Exception reading file {str(_filepath)}", exc_info=True)
        return lines

    @staticmethod
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

    @staticmethod
    def save_txt(filepath: Path | str, lines: Union[str, List[str]]) -> None:
        """
        Save a string or list of strings to a text file with exception handling.

        Args:
            filepath (Path): Path to save the file.
            lines (Union[str, List[str]]): Content to write. If string, converted to list.
        """
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
    def save_json(filepath: Path, data: Dict[str, Any]) -> None:
        """
        Save a dictionary to JSON, converting datetime objects to ISO strings.

        Args:
            filepath (Path): Path to save the JSON file.
            data (Dict[str, Any]): Data to save.
        """

        def default_serializer(obj):
            if isinstance(obj, DateTime):
                return obj.isoformat()
            return str(obj)

        with filepath.open("w", encoding="utf-8") as f:
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
