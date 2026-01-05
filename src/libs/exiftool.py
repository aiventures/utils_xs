"""Exiftool Wrapper."""

import os
import json
from json import JSONDecodeError
from config.myenv import MY_CMD_EXIFTOOL
from typing import Tuple, List, Dict, Optional, Union
from pathlib import Path
from copy import deepcopy
from config.colors import C_0, C_B, C_E, C_F, C_H, C_I, C_L, C_P, C_PY, C_Q, C_S, C_T, C_W
from libs.helper import CmdRunner, Helper, Persistence, Transformer
from libs.geo import (
    GEOREVERSE_METADATA_JSON,
    IMAGE_SUFFIXES,
    F_GPX_MERGED,
    F_OFFSET_ENV,
    F_METADATA_EXIF,
    F_METADATA_EXIF_ENV,
)

# suffixes use in EXIFTOOL Comands
SUFFIX_ARGS = []
for ext in IMAGE_SUFFIXES:
    SUFFIX_ARGS.extend(["-ext", ext])

# Note in the BAT Files you need to activate CHCP 65001 to get the right characters in output
# this is the literal path to the exiftool executable
CMD_EXIFTOOL = MY_CMD_EXIFTOOL

# 3. EXIFTOOL command to geotag images based on a gps track
# https://exiftool.org/geotag.html
# exiftool -progress50 -json -jpg -tif -geosync=00:00:00 -geotag mygps.gpx <file/path>
# CMD_EXIFTOOL_GEOTAG = [CMD_EXIFTOOL, "-progress50", "-json"] + SUFFIX_ARGS

# 4. EXIFTOOL command to export existing GPS Coordinates as reverse Geo (addresses) from images as json in german
# Reverse Geotag Coordinates > Address:
# https://exiftool.org/geolocation.html
# https://exiftool.org/geolocation.html#Geotag
# WRITE https://exiftool.org/geolocation.html#Write
# Shows the geolocations as json file when there are GPS Coordinates available
# exiftool -api geolocation "-geolocation*" -lang de -json <file/path>
#  CMD_EXIFTOOL_GEOTAG = [CMD_EXIFTOOL, "-api", "geolocation", "-lang", "de", "-progress50", "-json"] + SUFFIX_ARGS

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


class ExifTool:
    """ExifTool Wrapper.
    Visit: https://exiftool.org/
    """

    def __init__(
        self,
        path: Optional[Union[str, Path]] = None,
        encoding: str = "latin",
        language: str = "de",
        f_exiftool: Optional[Union[str, Path]] = CMD_EXIFTOOL,
        f_gpx_merged: Optional[str] = F_GPX_MERGED,
        show_output: bool = True,
    ):
        # do a check whether f_exiftool points to a file
        self._is_instanciated: bool = True
        if f_exiftool is None or not Path(f_exiftool).is_file():
            print(f"{C_E}🚨 [ExifTool] class not having a correct exiftool executable{C_0}")
            return
        self._exiftool = str(f_exiftool)

        _path = Path.cwd()
        if path is not None:
            _path = Path(path)
        if not _path.is_dir():
            print(f"{C_E}🚨 [ImageOrganizer] No valid path {_path}{C_0}")
            self._is_instanciated = False
            return
        self._path: Path = _path.absolute()
        # file encoding might lead to issues on windows if not latin1 or cp1252
        # utf-8 struggles in my case
        self._encoding: str = encoding
        # output data
        self._show_output = show_output
        # language code
        self._language = language
        # add an f_gpx_merged path if it exists / use a default
        self._f_gpx_merged: Optional[Path] = None
        if f_gpx_merged is not None and _path.joinpath(f_gpx_merged).is_file():
            self._f_gpx_merged = _path.joinpath(f_gpx_merged)

    @property
    def is_instanciated(self):
        return self._is_instanciated

    def _print(self, s: str) -> None:
        """Output if flag is set"""
        if self._show_output:
            print(s)

    def get_reverse_geoinfo(self, latlon: Tuple | List, file: str = None, index: int = 0, show: bool = False) -> dict:
        """Using Exiftool Reverse Geo API get the reverse corrdinates"""
        out: Dict = {
            "idx": 1,
            "file": None,
            "lat_lon": None,
            "geo_reverse": {},
            "geo_info": None,
            "time_zone": None,
        }

        if not (isinstance(latlon, List) or isinstance(latlon, Tuple)):
            print(f"{C_E}🚨 get_exiftool_reverse_geoinfo, passed params need to be list or tuple{C_0}")
            return
        lat = round(float(latlon[0]), 6)
        lon = round(float(latlon[1]), 6)

        # populate the output dict
        if file:
            out["file"] = str(file)
        out["lat_lon"] = [lat, lon]

        # 5. EXIFTOOL to export reverse Geo Coordinates base on lat lon
        # exiftool -g3 -a -json -lang de -api geolocation=40.748817,-73.985428
        # - g3: Document group
        # -a Shows all duplicate tags instead of suppressing them.
        # -lang Localizes tag descriptions into German.
        # -api geolocation=40.748817,-73.985428 run ExifTool Geo API
        cmd_exiftool_reverse_geo = [self._exiftool, "-g3", "-a", "-json", "-lang", self._language, "-api"]

        lat_lon = f"geolocation={lat},{lon}"
        # TODO support other locales as well
        # cmd_exiftool_reverse = CMD_EXIFTOOL_REVERSE_GEO.copy()
        cmd_exiftool_reverse_geo.append(lat_lon)
        # cmd_exiftool_reverse.append(lat_lon)
        # get reverse geocoordinates

        reverse_geo_s = "".join(CmdRunner.run_cmd_and_print(cmd_exiftool_reverse_geo))

        geo_reverse = {}
        geo_info = "No Reverse Geo Info"
        if reverse_geo_s:
            try:
                geo_reverse = json.loads(reverse_geo_s)[0]
                # print(json.dumps(reverse_geo, indent=4))
                geo_reverse = geo_reverse.get("Main", {})
                out["geo_reverse"] = geo_reverse
                city = geo_reverse.get("GeolocationCity")
                region = geo_reverse.get("GeolocationRegion")
                subregion = geo_reverse.get("GeolocationSubregion")
                time_zone = geo_reverse.get("GeolocationTimeZone", "Europe/Berlin")
                distance = geo_reverse.get("GeolocationDistance")
                bearing = geo_reverse.get("GeolocationBearing")
                geo_info = f"{distance}, {bearing}° to {city}/{subregion}/{region}"
                out["geo_info"] = geo_info
                out["time_zone"] = time_zone
                if show:
                    print(
                        f"\n{C_T}### OSM Coordinates {C_F}[{out['file']}] {C_Q}{out['lat_lon']}, {C_H}{geo_info} ({time_zone}){C_0}"
                    )
            except (JSONDecodeError, IndexError) as e:
                print(f"{C_E}🚨 Error occured during parsing OSM Coordinates [{latlon}], {e}")
                return None

        return out

    def cmd_export_meta(self, recursive: bool = False) -> list:
        """creates the exiftool command to export image data as json"""
        # command to export all exifdata in groups as json for given suffixes
        # progress is shown every 50 images
        # the c command is to format gps coordinates as decimals

        # 2. EXIFTOOL command to export metadata
        # exiftool -r -g -c %.6f -progress 50 -json -<extensions> ....

        exiftool_cmd = [self._exiftool]
        if recursive:
            exiftool_cmd.append("-r")
        exiftool_cmd.extend(["-g", "-c", "'%.6f'", "-progress50", "-json"])
        exiftool_cmd += SUFFIX_ARGS
        exiftool_cmd.append(str(self._path))
        return exiftool_cmd

    def export_metadata(
        self, f_metadata: str = F_METADATA_EXIF, f_metadata_env: str = F_METADATA_EXIF_ENV, recursive: bool = False
    ) -> List:
        """creates a json containing all metadata exif alongside with an env file that
        will store the path to the metadata file
        if recursive flag is set it will also create metadata for all
        subfolders
        """
        exif_cmd = self.cmd_export_meta(recursive)
        print(f"{C_H}    Create Metadata: {C_PY}[{exif_cmd}]{C_0}")
        f_metadata_exif = self._path.joinpath(f_metadata)
        output = CmdRunner.run_cmd_and_stream(exif_cmd, f_metadata_exif)
        Persistence.save_txt(self._path / f_metadata_env, str(f_metadata_exif))
        return output

    def read_geosync_from_env(self) -> str:
        """reads the offset string from the env file"""

        # get the geosync offset (previously written), with a default of 00:00:00
        f_offset = self._path.joinpath(F_OFFSET_ENV)
        lines = Persistence.read_txt_file(f_offset)
        t_offset = "+00:00:00" if len(lines) == 0 else lines[0]
        return f"-geosync={t_offset}"

    def create_gps_metadata_from_gpx(self) -> list:
        """creates the exiftool command to create gpx data in image files

        Returns:
        bool: True if the command succeeded, False otherwise.
        """

        # EXIFTOOL command to export existing GPS Coordinates as reverse Geo (addresses) from images as json in german
        # Reverse Geotag Coordinates > Address:
        # https://exiftool.org/geotag.html
        # https://exiftool.org/geolocation.html
        # https://exiftool.org/geolocation.html#Geotag
        # WRITE https://exiftool.org/geolocation.html#Write
        # Shows the geolocations as json file when there are GPS Coordinates available
        # exiftool -api geolocation "-geolocation*" -lang de -json <file/path>
        exif_cmd = [
            self._exiftool,
            "-api",
            "geolocation",
            "-lang",
            self._language,
            "-progress50",
            "-json",
        ] + SUFFIX_ARGS

        # use current path or input path
        p_work = self._path

        if self._f_gpx_merged is None:
            self._print(
                f"{C_H}No gpx file {self._f_gpx_merged} found, skip processing of creating gps based on gpx{C_0}"
            )
            return

        # get the geosync offset (previously written), with a default of 00:00:00
        geosync_tag = self.read_geosync_from_env()
        # command to geotag all elements in folder using an offset
        additional_params = [geosync_tag, "-geotag", self._f_gpx_merged, str(p_work)]
        exif_cmd.extend(additional_params)
        # exif_cmd.append(additional_params)
        output = CmdRunner.run_cmd_and_print(exif_cmd)

        return output

    def get_exiftool_create_gps_metadata_from_gpx(self) -> list:
        """creates the exiftool command to create gpx data in image files

        Returns:
        list: Output List
        """

        # use current path or input path
        p_work = self._path

        if self._f_gpx_merged is None:
            print(f"{C_H}No gpx file {self._f_gpx_merged} found, skip processing of creating gps based on gpx{C_0}")
            return

        # get the geosync offset (previously written), with a default of 00:00:00
        geosync = self.read_geosync_from_env()

        # command to geotag all elements in folder using an offset
        # exiftool -progress50 -json -jpg -tif ... -geosync=00:00:00 -geotag mygps.gpx <file/path>

        # exif_cmd = CMD_EXIFTOOL_GEOTAG.copy()
        exif_cmd = [self._exiftool, "-progress50", "-json", f"-geosync={geosync}", "-geotag", self._f_gpx_merged]
        exif_cmd += SUFFIX_ARGS
        exif_cmd.append(str(p_work))

        # additional_params = [geosync, "-geotag", f_gpx_merged, str(p_work)]
        # exif_cmd.extend(additional_params)
        # exif_cmd.append(additional_params)
        output = CmdRunner.run_cmd_and_print(exif_cmd)

        return output

    def get_original_datetime(self, f: Optional[Union[str, Path]]) -> Optional[str]:
        """gets the original datetime of an image"""
        _f = Path(str(f))
        cwd = Path(os.getcwd())
        if f is None or not _f.is_file():
            print(f"{C_E}🚨 [ExifTool] get_original_datetime, no valid file [{_f}]")
            return

        # run in path
        _p = _f.parent if _f.is_absolute() else self._path
        os.chdir(_p)
        _f = _f.name

        # Step 2: Run exiftool extracting Original DateTime Original
        # exiftool.exe -SubSecDateTimeOriginal -b "<path>\gps.jpg"
        cmd = [self._exiftool, "-SubSecDateTimeOriginal", "-b"]
        # we need to add the encoding to handle special chars in filenames
        cmd.extend(["-charset", f"filename={self._encoding}"])
        cmd.append(str(_f))
        self._print(f"{C_T}Running exiftool command:{C_0} {cmd}")
        cmd_output = CmdRunner.run_cmd_and_print(cmd)
        timestamp_image = None

        if not cmd_output:
            print(f"{C_E}🚨 Exiftool command [{cmd}] failed.{C_0}")
            return None
        else:
            try:
                timestamp_image = cmd_output[0]
                self._print(f"{C_T}Got Timestamp from {C_F}[{f.name}] {C_H}[{timestamp_image}]{C_0}")
            except IndexError:
                print(f"{C_E}🚨 [ExifTool] Couldn't parse timetamp from [{str(f)}]")
        os.chdir(cwd)
        return timestamp_image
