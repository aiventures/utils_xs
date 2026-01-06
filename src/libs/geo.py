"""Geo some structrue definitions and basic calculations"""

import re
from typing import Dict
from math import pi
from math import sin
from math import sqrt
from math import cos
from math import asin
from math import floor


# from image_meta.util import Util
# from image_meta.persistence import Persistence
from datetime import datetime as DateTime
import datetime

# from datetime import timedelta
# import requests
import traceback

# reverse geo
REVERSE_GEO_INFO = "reverse_geo_info"
EXTERNAL_KEY_MAP = "external_key_map"
EXTRA = "extra"

# image_organizer

# Files To Be Used To Be added to the central F_METADATA FILE
# General approach is to reference file in env files so to be flexible w.r.t. naming
# CONFIG_FILES
DATETIME = "datetime"
DATETIME_ORIGINAL = "SubSecDateTimeOriginal"
DATETIME_ADJUSTED = "DateTimeAdjusted"
FILES = "files"
FILENAME = "FileName"
FILEPATH = "FilePath"
FILES_ENV = "files_env"
METADATA_EXIF = "metadata_exif"
METADATA_IPTC = "metadata_iptc"
METADATA_GEO = "metadata_geo"
METADATA_EXIFTOOL = "metadata_exiftool"

METADATA_OSM = "metaddata_osm"
TIMESTAMP_IMAGE = "timestamp_image"
IMAGE_GEO_INFO = "image_geo_info"
OFFSET = "offset"
OFFSET_SECS = "offset_secs"
OFFSET_STR = "offset_str"
OFFSET_CAM = "offset_cam"
OFFSET_GPS = "offset_gps"
LAT_LON = "lat_lon"
LAT_LON_ORIGIN = "lat_lon_origin"
GPS_TRACK = "gps_track"
TRACK = "track"
GPS_METADATA = "gps_metadata"
TIMESTAMP_UTC = "timestamp_utc"
TIMEZONE = "timezone"
TIMEZONE_DEFAULT = "Europe/Berlin"
# etxra gps data
ELEVATION = "elevation"
HEARTRATE = "heartrate"
TEMPERATURE = "temperature"

# All Metadata (the json template below)
CONFIG_F_METADATA_ENV = "f_metadata_env"
CONFIG_F_METADATA = "f_metadata"
F_METADATA = "metadata.json"
F_METADATA_ENV = "metadata.env"

# Image Metadata
CONFIG_F_METADATA_EXIF_ENV = "f_metadata_exif_env"
F_METADATA_EXIF_ENV = "metadata_exif.env"
CONFIG_F_METADATA_EXIF = "f_metadata_exif"
F_METADATA_EXIF = "metadata_exif.json"

# Reverse Geo Metadata from Nominatim
IMAGE_REVERSE_GEO_INFO = "image_reverse_geo_info"
CONFIG_F_METADATA_GEO_REVERSE_ENV = "f_metadata_geo_reverse_env"
F_METADATA_GEO_REVERSE = "metadata_geo_reverse.json"
CONFIG_F_METADATA_GEO_REVERSE = "f_metadata_geo_reverse"

# Image containing the timestamp and the GPS Image
# Timestamp files to calculate offset
# T_CAMERA - T_GPS = T_OFFSET
# default image for image containing camera timestamp
F_TIMESTAMP_IMG_DEFAULT = "gps.jpg"

CONFIG_F_TIMESTAMP_IMG_ENV = "f_timestamp_img_env"
CONFIG_F_TIMESTAMP_IMG = "f_timestamp_img"
CONFIG_F_OFFSET_ENV = "f_offset_env"
CONFIG_F_OFFSET_SECS_ENV = "f_offset_secs_env"
CONFIG_OFFSET_SECS = "offset_secs"
CONFIG_OFFSET_STR = "offset_str"
F_OFFSET_ENV = "offset.env"
F_OFFSET_SECS_ENV = "offset_sec.env"
CONFIG_F_TIMESTAMP_CAMERA_ENV = "f_timestamp_camera_env"
CONFIG_F_TIMESTAMP_GPS_ENV = "f_timestamp_gps_env"
CONFIG_F_TIMESTAMP_CAMERA = "f_timestamp_camera"
CONFIG_F_TIMESTAMP_GPS = "f_timestamp_gps"
CONFIG_TIMESTAMP_CAMERA = "timestamp_camera"
CONFIG_TIMESTAMP_GPS = "timestamp_gps"

# exiftool import metadata definitions
EXIFTOOL_METADATA_IMPORT = "exiftool_metadata_import"
CONFIG_F_EXIFTOOL_IMPORT_ENV = "f_exiftool_import_env"
CONFIG_F_EXIFTOOL_IMPORT = "f_exiftool_import"

F_TIMESTAMP_IMG_ENV = "timestamp_img.env"
F_TIMESTAMP_GPS = "timestamp_gps.json"
F_TIMESTAMP_CAMERA = "timestamp_camera.json"
F_EXIFTOOL_IMPORT = "exiftool_import.json"

# OpenStretMap Configuration
CONFIG_F_OSM_ENV = "f_osm_env"
CONFIG_F_OSM = "f_osm"
F_OSM_ENV = "osm.env"  # contains name of osm config file
F_OSM = "osm.json"

# Geotracker GPX DATA
CONFIG_F_GPX_MERGED_ENV = "f_gpx_merged_env"
CONFIG_F_GPX_MERGED = "f_gpx_merged"
CONFIG_F_GPX_MERGED_JSON = "f_gpx_merged_json"
F_GPX_MERGED_ENV = "gpx_merged.env"
F_GPX_MERGED = "gpx_merged.gpx"
F_GPX_MERGED_JSON = "gpx_merged.json"

# GEOREVERSE STRUCTURE
GEOREVERSE_METADATA_JSON: Dict = {
    "idx": 1,
    "file": None,
    "lat_lon": None,
    "geo_reverse": {},
    "geo_info": None,
    "time_zone": None,
}

# Paths from environemt
# Define image suffixes and default paths
IMAGE_SUFFIXES = ["jpg", "jpeg", "raf", "dng"]


class Geo:
    """Geo calculations"""

    RADIUS_EARTH = 6371  # Earth Radius in kilometers

    GEOHACK_URL = "https://geohack.toolforge.org/geohack.php?params="
    NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"
    NOMINATIM_REVERSE_PARAMS = {
        "format": "geojson",
        "lat": "0",
        "lon": "0",
        "zoom": "18",
        "addressdetails": "18",
        "accept-language": "de",
    }

    @staticmethod
    def latlon2cartesian(lat_lon, radius=RADIUS_EARTH):
        """ "transforms (lat,lon) to cartesian coordinates (x,y,z)"""
        lat_deg, lon_deg = lat_lon
        lat = (pi / 180) * lat_deg
        lon = (pi / 180) * lon_deg
        lat_radius = cos(lat) * radius
        x = sin(lon) * lat_radius
        y = cos(lon) * lat_radius
        z = sin(lat) * radius
        return (x, y, z)

    @staticmethod
    def get_distance(latlon1, latlon2, radius=RADIUS_EARTH, show=False, cartesian_length=False):
        """calculates distance (wither cartesian (default) or arc segment length)
        of two tuples (lat,long) into cartesian in kilometers"""
        c1 = Geo.latlon2cartesian(latlon1)
        c2 = Geo.latlon2cartesian(latlon2)
        delta_c = [coord[1] - coord[0] for coord in list(zip(c2, c1))]
        # distance and arc segment
        distance = sqrt(sum([delta**2 for delta in list(delta_c)]))
        if cartesian_length is False:
            distance_arc = 2 * radius * asin((distance / 2) / radius)
            if show is True:
                print("Arc Distance:", distance_arc, "Distance:", distance, " Difference:", (distance_arc - distance))
            distance = distance_arc
        if show is True:
            print("Delta Coordinates (X,Y,Z):", delta_c, "\n Distance:", distance)
        return distance

    @staticmethod
    def get_exifmeta_from_latlon(latlon, altitude=None, timestamp: int = None):
        """Creates Exif Metadata Dictionary for GPS Coordinates"""
        geo_dict = {}

        if not (isinstance(latlon, list) or isinstance(latlon, tuple)):
            return geo_dict

        lat, lon = latlon

        latref = "N"
        lonref = "E"

        if lat < 0:
            latref = "S"
        if lon < 0:
            lonref = "W"

        geo_dict["GPSLatitude"] = lat
        geo_dict["GPSLatitudeRef"] = latref
        geo_dict["GPSLongitude"] = lon
        geo_dict["GPSLongitudeRef"] = lonref

        if altitude is not None:
            geo_dict["GPSAltitudeRef"] = "above"
            geo_dict["GPSAltitude"] = round(altitude, 0)

        if isinstance(timestamp, int):
            geo_dict["GPSDateStamp"] = DateTime.fromtimestamp(timestamp, datetime.timezone.utc).strftime("%Y:%m:%d")
            geo_dict["GPSTimeStamp"] = DateTime.fromtimestamp(timestamp, datetime.timezone.utc).strftime("%H:%M:%S")

        return geo_dict

    @staticmethod
    def dec2geo(dec):
        """converts decimals to geo type format"""
        degrees = round(floor(dec), 0)
        minutes = round(floor(60 * (dec - degrees)), 0)
        rest = dec - degrees - (minutes / 60)
        seconds = round(rest * 60 * 60)
        return (degrees, minutes, seconds)

    @staticmethod
    def latlon2geohack(latlon):
        """converts latlon to decimals in geohack format"""
        try:
            latlon = list(map(lambda n: (round(n, 7)), latlon))
            lat, lon = latlon
        except:
            return None
        lat_ref = "N"
        lon_ref = "E"
        if lat < 0:
            lat_ref = "S"
        if lon < 0:
            lon_ref = "W"
        coord_s = "_".join([str(abs(lat)), lat_ref, str(abs(lon)), lon_ref])
        return coord_s

    @staticmethod
    def geohack2dec(geohack: str):
        """converts geohack string into geo tuple"""
        latlon_s = geohack.split("_")
        lat_ref = latlon_s[3]
        lon_ref = latlon_s[7]
        lat_f = 1.0
        lon_f = 1.0
        if lat_ref == "S":
            lat_f = -1.0
        if lon_ref == "W":
            lat_f = -1.0
        coords_geo = list(map(lambda f: float(f), [*latlon_s[:3], *latlon_s[4:7]]))
        coords = (
            (lat_f * (coords_geo[0] + (coords_geo[1] / 60) + (coords_geo[2] / 3600))),
            (lon_f * (coords_geo[3] + (coords_geo[4] / 60) + (coords_geo[5] / 3600))),
        )
        return coords

    @staticmethod
    def latlon_from_osm_url(url: str):
        """extracts the map part latlon information from an osm link
        https://www.openstreetmap.org/#map=xx/lat/lon
        https://www.openstreetmap.org/search?query=qd#map=xx/lat/lon"
        """
        latlon = None
        regex_osm = "map\=(\d+)\/(.+)?\/(.+)"
        osm_matches = re.findall(regex_osm, url)
        if isinstance(osm_matches, list) and len(osm_matches) == 1:
            osm_matches = osm_matches[0][1:]
            # extract latlon info as float number
            try:
                osm_matches = [float(osm_match) for osm_match in osm_matches]
                latlon = osm_matches
            except Exception:
                print(f"--- EXCEPTION latlon_from_osm_url: {url} ---")
                print(traceback.format_exc())
                return None
        return latlon

    @staticmethod
    def latlon2osm(latlon, detail=18):
        """converts latlon to osm url"""
        # https://www.openstreetmap.org/#map=<detail>/<lat>/<lon>
        if not (isinstance(latlon, list) or isinstance(latlon, tuple)):
            return None

        detail = str(detail)
        lat = str(latlon[0])
        lon = str(latlon[1])
        return f"https://www.openstreetmap.org/#map={detail}/{lat}/{lon}"

    # @staticmethod
    # def get_nearest_gps_waypoint(
    #     latlon_ref, gps_fileref, date_s_ref=None, tz="Europe/Berlin", dist_max=1000, debug=False
    # ) -> dict:
    #     """Gets closest GPS point in a gps track for given latlon coordinate and time difference if datetime string is given
    #     latlon_ref  -- latlon coordinates (list or tuple)
    #     gps_fileref -- filepath to gpsx file
    #     date_s_ref  -- datetime of reference point  "%m:%d:%Y %H:%M:%S"
    #     tz          -- timezone (pytz.tzone)
    #     distmax     -- maximum distance in m whether point will be used as minimum distance (default 1000m)
    #     debug       -- outpur additional information
    #     """
    #     gps_min = {}
    #     dist_min = dist_max
    #     tz = "Europe/Berlin"
    #     dt_ref = Util.get_datetime_from_string(datetime_s=date_s_ref, local_tz=tz)
    #     # geohack url
    #     url_geohack = Geo.GEOHACK_URL + Geo.latlon2geohack(latlon_ref)
    #     # load gps data
    #     gps_coords = Persistence.read_gpx(gpsx_path=gps_fileref)
    #     if not gps_coords:
    #         print(f"no gps data found in file {gps_fileref}")
    #         return gps_min
    #     num = len(gps_coords.keys())
    #     timestamps = list(gps_coords.keys())
    #     timestamps.sort()
    #     timestamp_min = min(timestamps)
    #     timestamp_max = max(timestamps)
    #     # utc from (utc) timestamp
    #     dt_min_utc = datetime.utcfromtimestamp(timestamp_min)
    #     dt_max_utc = datetime.utcfromtimestamp(timestamp_max)
    #     # get localized datetime
    #     dt_min = Util.get_localized_datetime(dt_min_utc, tz_in="UTC", tz_out=tz)
    #     dt_max = Util.get_localized_datetime(dt_max_utc, tz_in="UTC", tz_out=tz)
    #     # get geo data
    #     geo_min = gps_coords[timestamp_min]
    #     latlon_min = (geo_min["lat"], geo_min["lon"])
    #     geo_max = gps_coords[timestamp_max]
    #     latlon_max = (geo_max["lat"], geo_max["lon"])
    #     if debug:
    #         dist_max = int(1000 * Geo.get_distance(latlon_ref, latlon_max))
    #         dist_min = int(1000 * Geo.get_distance(latlon_ref, latlon_min))
    #         dist_track = int(1000 * Geo.get_distance(latlon_max, latlon_min))
    #         print(
    #             f"--- Track '{geo_min.get('track_name', 'Unknown Track')}': {num} data points, duration {dt_max - dt_min}"
    #         )
    #         print(f"    Timezone: {tz}")
    #         print(f"    Start latlon: {latlon_min} / Datetime {dt_min}")
    #         print("                  ", (Geo.GEOHACK_URL + Geo.latlon2geohack(latlon_min)))
    #         print(f"    End latlon: {latlon_max} / Datetime {dt_max}")
    #         print("                ", (Geo.GEOHACK_URL + Geo.latlon2geohack(latlon_max)))
    #         print(f"--- Reference latlon: {latlon_ref} / Datetime {dt_ref}")
    #         print("    Geohack url:", url_geohack)
    #         print(f"--- Distance: start-ref {dist_min}m, end-ref {dist_max}m, start-end {dist_track}m")
    #     timestamp_min = None
    #     for timestamp, gps_coord in gps_coords.items():
    #         latlon = [gps_coord["lat"], gps_coord["lon"]]
    #         dist = int(1000 * Geo.get_distance(latlon_ref, latlon))
    #         if dist < dist_min:
    #             dist_min = dist
    #             datetime_min_utc = datetime.utcfromtimestamp(timestamp)
    #             datetime_min = Util.get_localized_datetime(datetime_min_utc, tz_in="UTC", tz_out="Europe/Berlin")
    #             gps_min["timestamp_utc"] = timestamp
    #             gps_min["datetime"] = datetime_min
    #             gps_min["lat"] = gps_coord["lat"]
    #             gps_min["lon"] = gps_coord["lon"]
    #             gps_min["ele"] = gps_coord["ele"]
    #             gps_min["distance_m"] = dist_min
    #             if dt_ref is not None:
    #                 gps_min["timedelta_from_ref"] = int(timedelta.total_seconds(datetime_min - dt_ref))
    #             else:
    #                 gps_min["timedelta_from_ref"] = None
    #             gps_min["url_geohack"] = Geo.GEOHACK_URL + Geo.latlon2geohack(latlon)
    #     if gps_min.get("distance_m", dist_max) < dist_max:
    #         if debug:
    #             print(f"--- Nearest GPS Trackpoint")
    #             Util.print_dict_info(d=gps_min)
    #     else:
    #         print(f"no gps points found in vicinity of {dist_min} m")

    #     return gps_min
