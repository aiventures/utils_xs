"""transforms json structures to flattened json structure for usage with ExifTool
List of XMP Fields  https://exiftool.org/TagNames/XMP.html
List of IPTC Fields https://exiftool.org/TagNames/IPTC.html
        IPTC SPECS  https://iptc.org/standards/photo-metadata/iptc-standard/
        => "XMP exif Tags"
        => "XMP LocationDetails Struct"
        Note that the GPS elements of this structure are in the "exif" namespace.
"""

import os
from typing import Any, Optional, Tuple, Literal
from datetime import datetime as DateTime
import json
from libs.geo import Geo
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F, C_W

# get some properties from the environment / define it in the setenv.bat or a bash
# initialization script respectively. Use the template in /templates/myenv_template.bat
EXIFTOOL_AUTHOR = os.environ.get("MY_EXIFTOOL_AUTHOR", "UNKNWON AUTHOR")
EXIFTOOL_BYLINE_TITLE = os.environ.get("MY_EXIFTOOL_AUTHORTITLE", "Honorable")

# this is the expected sample json based on exiftool reverse geo API
SAMPLE_EXIFREVERSE = {
    "sample": {
        "geotrack_origin": "gpx",
        "metadata_geo": {
            "idx": 1,
            "file": "....",
            "lat_lon": [49.119948, 8.787893],
            "geo_reverse": {
                "GeolocationCity": "Zaisenhausen",
                "GeolocationRegion": "Baden-Württemberg",
                "GeolocationSubregion": "Regierungsbezirk Karlsruhe",
                "GeolocationCountryCode": "DE",
                "GeolocationCountry": "Bundesrepublik Deutschland",
                "GeolocationTim0eZone": "Europe/Berlin",
                "GeolocationFeatureCode": "PPLA4",
                "GeolocationFeatureType": "Seat of a Fourth-order Administrative Division",
                "GeolocationPopulation": 1800,
                "GeolocationPosition": "49.1067, 8.8128",
                "GeolocationDistance": "2.32 km",
                "GeolocationBearing": 118,
            },
            "geo_info": "2.32 km, 118° to Zaisenhausen/Regierungsbezirk Karlsruhe/Baden-Württemberg",
            "time_zone": "Europe/Berlin",
        },
        "gps_info": {
            "datetime_camera_exif": "2025:08:31 16:04:26.73+02:00",
            "offset": -286,
            "datetime_camera_utc": "2025-08-31T13:59:40.730000+00:00",
            "datetime_gps_utc": "2025-08-31T13:59:42+00:00",
            "timestamp_camera": 1756648780730,
            "timestamp_gps": 1756648782000,
            "timestamp_diff": -1.27,
        },
    }
}


# Note depending on category theres's diferent address attributes
# https://nominatim.org/release-docs/develop/api/Reverse/
# https://nominatim.org/release-docs/latest/api/Output/#addressdetails

# Examples
# City Place:
# https://www.openstreetmap.org/#map=17/48.778175/9.181369
# https://nominatim.openstreetmap.org/reverse?lat=48.778175&lon=9.181369&format=json&addressdetails=17
# {
#     "osm_type": "node",
#     "class": "tourism",
#     "type": "artwork",
#     "addresstype": "tourism",
#     "name": "Herkules",
#     "display_name": "Herkules, Leopoldo-Retti-Weg, Oberer Schlossgarten, Stuttgart-Mitte, Stuttgart, Baden-Württemberg, 70173, Deutschland",
#     "address": {
#         "tourism": "Herkules",
#         "road": "Leopoldo-Retti-Weg",
#         "neighbourhood": "Oberer Schlossgarten",
#         "suburb": "Stuttgart-Mitte",
#         "city": "Stuttgart",
#         "state": "Baden-Württemberg",
#         "ISO3166-2-lvl4": "DE-BW",
#         "postcode": "70173",
#         "country": "Deutschland",
#         "country_code": "de"
#     },
# }

# City Building
# https://www.openstreetmap.org/#map=19/48.780727/9.191953
# https://nominatim.openstreetmap.org/reverse?lat=48.780727&lon=9.191953&format=json&addressdetails=17
# {
#     "osm_type": "way",
#     "class": "building",
#     "place_rank": 30,
#     "addresstype": "building",
#     "name": "",
#     "display_name": "30, Haußmannstraße, Kernerviertel, Stuttgart-Mitte, Stuttgart, Baden-Württemberg, 70188, Deutschland",
#     "address": {
#         "house_number": "30",
#         "road": "Haußmannstraße",
#         "neighbourhood": "Kernerviertel",
#         "suburb": "Stuttgart-Mitte",
#         "city": "Stuttgart",
#         "state": "Baden-Württemberg",
#         "ISO3166-2-lvl4": "DE-BW",
#         "postcode": "70188",
#         "country": "Deutschland",
#         "country_code": "de"
#     },
# }

# Village
# https://www.openstreetmap.org/#map=19/48.630626/9.155566
# https://nominatim.openstreetmap.org/reverse?lat=48.630626&lon=9.15566&format=json&addressdetails=17
# {
#     "class": "building",
#     "addresstype": "building",
#     "display_name": "13, Wacholderweg, Glashütte, Waldenbuch, Gemeindeverwaltungsverband Waldenbuch/Steinenbronn, Landkreis Böblingen, Baden-Württemberg, 71111, Deutschland",
#     "address": {
#         "house_number": "13",
#         "road": "Wacholderweg",
#         "village": "Glashütte",
#         "town": "Waldenbuch",
#         "municipality": "Gemeindeverwaltungsverband Waldenbuch/Steinenbronn",
#         "county": "Landkreis Böblingen",
#         "state": "Baden-Württemberg",
#         "ISO3166-2-lvl4": "DE-BW",
#         "postcode": "71111",
#         "country": "Deutschland",
#         "country_code": "de"
#     },
# }

# Forest Way
# https://www.openstreetmap.org/#map=18/48.623539/9.153958
# https://nominatim.openstreetmap.org/reverse?lat=48.623539&lon=9.153958&format=json&addressdetails=17
# {
#     "class": "tourism",
#     "addresstype": "tourism",
#     "display_name": "Vom Suchen und Finden, Dettenhäuser Weg, Aichtal, Landkreis Esslingen, Baden-Württemberg, 72631, Deutschland",
#     "address": {
#         "tourism": "Vom Suchen und Finden",
#         "road": "Dettenhäuser Weg",
#         "municipality": "Aichtal",
#         "county": "Landkreis Esslingen",
#         "state": "Baden-Württemberg",
#         "ISO3166-2-lvl4": "DE-BW",
#         "postcode": "72631",
#         "country": "Deutschland",
#         "country_code": "de"
#     },
# }

SAMPLE_GEOREVERSE = {
    "sample": {
        "place_id": 415916694,
        "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
        "osm_type": "way",
        "osm_id": 30045902,
        "lat": "49.1199546",
        "lon": "8.7878757",
        "category": "highway",
        "type": "unclassified",
        "place_rank": 26,
        "importance": 0.05338245441367205,
        "addresstype": "road",
        "name": "",
        "display_name": "Bahnbrücken, Rohrbach am Gießhübel, Bahnbrücken, Kraichtal, Landkreis Karlsruhe, Baden-Württemberg, 76703, Deutschland",
        "address": {
            "suburb": "Bahnbrücken",
            "village": "Rohrbach am Gießhübel",
            "municipality": "Kraichtal",
            "county": "Landkreis Karlsruhe",
            "state": "Baden-Württemberg",
            "ISO3166-2-lvl4": "DE-BW",
            "postcode": "76703",
            "country": "Deutschland",
            "country_code": "de",
        },
        "boundingbox": ["49.1199335", "49.1344446", "8.7878690", "8.8526804"],
        "extra": {
            "FileName": "20250831_Bahnbrücken_0136.jpg",
            "timestamp_utc": 1756648782000,
            "timezone": "Europe/Berlin",
            "datetime": "2025:08:31 15:59:42",
            "elevation": 209,
            "heartrate": 127,
        },
    }
}

# Tags to be Populated from EXIFTOOL / Example
# Use the following commands as batch file to remove and recreate metadata
# for test.jpg file
# echo delete metadata
# exiftool -all= test.jpg
# exiftool -json test.jpg -G1 -c '%.6f'
# echo update metadata
# exiftool -overwrite_original -json=test.json test.jpg
# exiftool -json test.jpg -G1 -c '%.6f'
# echo show hugo segments
# exiftool -json test.jpg -G1 -c '%.6f' | grep -i hugo
SAMPLE_METADATA_EXIFTOOL_TAGS = [
    {
        "SourceFile": "test.jpg",
        # IFD Segment https://exiftool.org/TagNames/EXIF.html
        "ImageTitle": "hugoImageTitle ExifIFD",  # MAPPED
        "ImageDescription": "HugoImageDescription_ifd0",  # MAPPED
        # GPS Segment https://exiftool.org/TagNames/GPS.html
        "GPSLatitude": 48.123456,  # MAPPED
        "GPSLatitudeRef": "N",  # MAPPED
        "GPSLongitude": 8.765432,  # MAPPED
        "GPSLongitudeRef": "E",  # MAPPED
        "GPSAltitude": 120.5,  # MAPPED
        "GPSAltitudeRef": 1,  # MAPPED
        # IPTC Segment https://exiftool.org/TagNames/IPTC.html
        # the following IPTC attributes are also used in the IRFAN VIEW TABS
        # IRFAN Description TAB
        "ObjectName": "hugoObjectName IPTC",  # MAPPED
        "By-lineTitle": "hugo by-line title IPTC",  # MAPPED
        "By-line": "hugo by-line Henrik Fessler_IPTC",  # MAPPED
        "CopyrightNotice": "(C) HUGO COPYRIGHT NOTICE IPTC",  # MAPPED
        "Caption-Abstract": "HUGO CAPTION ABSTRACT Longtext IPTC",  # MAPPED
        "Writer-Editor": "HUGO WRITER EDITOR IPTC",  # MAPPED
        "Headline": "hugoheadline IPTC",  # MAPPED
        "SpecialInstructions": "HugoSpecialInstructions IPTC",  # MAPPED
        # IRFAN KEYWORDS TAB
        "Keywords": ["hugo1 IPTC", "hugo2"],  # TODO
        "Category": "XYZ",  # only three letters # MAPPED to NT1
        "SupplementalCategories": ["hugo sup1 iptc"],  # NOT SUPPLIED
        "Urgency": 6,  # MAPPED To 6
        # IRFAN Credits/Origin Tab
        "Credit": "HUGO CREDIT IPTC",  # MAPPED
        "Source": "HugoSource_IPTC",  # mapped to own photography
        "DateCreated": "2099:03:29 23:55:58 IPTC",  # MAPPED
        "City": "HugoCity_IPTC",  # MAPPED
        "Sub-location": "HUGO SUB LOCATION_IPTC",
        "Province-State": "HUGO Baden-Württemberg IPTC",  # MAPPED
        "Country-PrimaryLocationName": "HUGO PRIMARY LOCATION NAME IPTC",  # MAPPED
        "OriginalTransmissionReference": "HUGOI TRANSMISSION timedate IPTC",  # MAPPED
        # OTHER IPTC
        "Country-PrimaryLocationCode": "de",  # MAPPED
        ###### XMP https://exiftool.org/TagNames/XMP.html
        # XMP Photoshop
        "CaptionWriter": "Hugo Caption Writer xmp photoshop",  # MAPPED
        "Country": "HugoDeutshcland_xmp_photoshop_country",  # MAPPED
        # XMP iptcCore
        "CountryCode": "de",  # MAPPED
        "Location": "HugoLocation_xmp_iptcCore",  # MAPPED
        "CreatorWorkURL": "hugocreatorworkurl__xmp_iptcCore",  # MAPPED
        "IntellectualGenre": "hugoIntellectualGenre XMP-iptcCore",  # MAPPED
        # XMP DC
        "Contributor": "HugoContributor_xmp_dc",  # MAPPED
        "Creator": "HugoCreator_xmp_dc",  # MAPPED
        "Description": "HugoDescription_xmp_dc",  # MAPPED
        "Rights": "HugoRights_xmp_dc",  # MAPPED
        "Subject": "HugoSubject_xmp_dc",  # MAPPED
        "Title": "HugoTitle_xmp_dc",  # MAPPED
        # XMP-xmp
        "Rating": 3,  # MAPPED
        "BaseURL": "hugobaseurl_xmp_xmp",  # MAPPED
    }
]

# ATTRIBUTES TO BE USED
FILE = "file"
AUTHOR = "author"
AUTHORTITLE = "authortitle"
RIGHTS = "rights"
COPYRIGHT = "copyright"
URGENCY = "urgency"
SOURCE = "source"
RATING = "rating"
ORIGINAL_TRANSMISSION_REF = "original_transmission_ref"
# https://www.iptc.org/std/photometadata/documentation/userguide/#_intellectual_genre_legacy
GENRE = "genre"
DATE_CREATED = "date_created"
KEYWORDS = "keywords"

# IPTC Category NT1 https://vocabularyserver.com/mediatopic/index.php?tema=1&/arts-culture-and-entertainment
IPTC_CATEGORY = "iptc_category"
DESCRIPTION = "description"
DATETIME = "datetime"
COUNTRY = "country"
COUNTRY_CODE = "country_code"
STATE = "state"
ZIP_CODE = "zip_code"
SUBREGION = "subregion"
LOCATION = "location"
CITY = "city"
METADATA_GEO = "metadata_geo"
GEO_URL = "geo_url"

LAT = "lat"
LON = "lon"
LAT_ORIENTATION = "lat_orientation"
LON_ORIENTATION = "lon_orientation"
ELEVATION = "elevation"
ELEVATION_REF = "elevation_ref"

# labels to extract dta from json
METADATA_SEGMENT = [METADATA_GEO, "address"]
COUNTRY_LABELS = ["GeolocationCountry", "country"]
COUNTRYCODE_LABELS = ["GeolocationCountryCode", "country_code"]
STATE_LABELS = ["GeolocationRegion", "state"]
ZIP_LABELS = ["postcode"]
# for nominatim the json definitions are a bit sketchy so we'll take a first match approach here
SUBREGION_LABELS = ["GeolocationSubregion", "municipality", "county", "suburb", "city", "town", "village", "hamlet"]
CITY_LABELS = ["GeolocationCity", "city", "village", "town", "hamlet"]

# MAP To Populate EXIFTOOL Metadata fields from input fields
EXIFTOOL_MAP = {
    # fixed values
    FILE: ["SourceFile"],
    AUTHOR: ["By-line", "Writer-Editor", "Creator", "Contributor", "Credit", "CaptionWriter"],
    AUTHORTITLE: ["By-lineTitle"],
    COPYRIGHT: ["CopyrightNotice"],
    IPTC_CATEGORY: ["Category"],
    GENRE: ["IntellectualGenre"],
    URGENCY: ["Urgency"],
    RATING: ["Rating"],
    RIGHTS: ["Rights"],
    ORIGINAL_TRANSMISSION_REF: ["OriginalTransmissionReference"],
    DATE_CREATED: ["DateCreated"],
    DESCRIPTION: [
        "ImageTitle",
        "ImageDescription",
        "ObjectName",
        "Caption-Abstract",
        "Headline",
        "Title",
        "Subject",
        "Description",
    ],
    LAT: ["GPSLatitude"],
    LON: ["GPSLongitude"],
    LAT_ORIENTATION: ["GPSLatitudeRef"],
    LON_ORIENTATION: ["GPSLongitudeRef"],
    ELEVATION: ["GPSAltitude"],
    ELEVATION_REF: ["GPSAltitudeRef"],
    GEO_URL: ["SpecialInstructions", "BaseURL", "CreatorWorkURL"],
    COUNTRY: ["Country-PrimaryLocationName", "Country"],
    COUNTRY_CODE: ["CountryCode", "Country-PrimaryLocationCode"],
    STATE: ["Province-State"],
    LOCATION: ["City", "Location"],
    # not needed right now
    # KEYWORDS:["Keywords"]
    # ZIP_CODE: [],
    # SUBREGION: [],
}


class GeoMetaTransformer:
    """class to transform geo data"""

    def __init__(self, filename: str, meta_dict: dict):
        """Constructor"""
        # filename
        self._filename = filename
        # gets the meta dict
        self._meta_dict = meta_dict
        # flag if reverse geo metadata is from exiftool (true) or from nominatim (false)
        self._metadata_type: Literal["exiftool", "georeverse_api", "undefined"] = "undefined"
        self._meta_geo = self._get_geo_meta()
        if self._metadata_type == "undefined":
            print(f"{C_W} No Proper Geo Metadata detected")

    def _get_geo_meta(self) -> dict:
        """gets the address metadata from meta dictionary depending on passed type"""
        _metadata_geo = self._meta_dict.get(METADATA_GEO)
        if _metadata_geo is not None:
            self._metadata_type = "exiftool"
            return _metadata_geo

        _metadata_geo = self._meta_dict.get("address", {})
        if _metadata_geo is not None:
            self._metadata_type = "georeverse_api"
        return _metadata_geo

    def get_display_name(self) -> str:
        """gets the long display name from the meta data"""
        if self._metadata_type == "exiftool":
            return self._meta_dict.get("display_name", "NO DISPLAY NAME")
        elif self._metadata_type == "georeverse_api":
            return self._meta_geo.get("geo_info", "NO DISPLAY NAME")

        return "NO DISPLAY NAME"

    def get_value_from_meta(self, attribute_list: list[str]) -> Optional[Any]:
        """Gets a value from a dict upon first occurence of a value"""
        for attribute in attribute_list:
            if self._meta_dict.get(attribute) is not None:
                return self._meta_dict.get(attribute)
        return None

    def _get_gps_data_exiftool(self) -> Optional[Tuple[float, float, float]]:
        """gets the lat lon altitude coordinates from exiftool geo reverse"""
        if self._metadata_type != "exiftool":
            return None
        try:
            lat, lon = self._meta_geo.get("lat_lon")
            lat = float(lat)
            lon = float(lon)
        except (ValueError, IndexError):
            print(f"{C_E}🚨[GeTransformer] GPS Data Conversion error {C_0}")
            return None
        # no altitude for this case
        return (lat, lon, 0.0)

    def _get_gps_data_georeverse(self) -> Optional[Tuple[float, float, float]]:
        """gets the lat lon altitude coordinates from exiftool geo reverse"""
        if self._metadata_type != "georeverse_api":
            return None

        try:
            lat = float(self._meta_dict.get("lat"))
            lon = float(self._meta_dict.get("lat"))
            ele = float(self._meta_dict.get("extra", {}).get("elevation", 0.0))
        except (ValueError, IndexError):
            print(f"{C_E}🚨[GeoTransformer] GPS Data Conversion error {C_0}")
            return None
        return (lat, lon, ele)

    def get_gps_data(self) -> Optional[Tuple[float, float, str, str, float]]:
        """returns lat,lon,orientation lat lon,altitude geo data"""

        lat = None
        lon = None
        elevation = None
        try:
            if self._metadata_type == "exiftool":
                lat, lon, elevation = self._get_gps_data_exiftool()
            elif self._metadata_type == "georeverse_api":
                lat, lon, elevation = self._get_gps_data_georeverse()
            else:
                print(f"{C_E}🚨[GeoTransformer] No GPS Data found {C_0}")
        # try exifreverse data first
        except (ValueError, IndexError):
            print(f"{C_E}🚨[GeoTransformer] No GPS Data found {C_0}")
            return None

        lat_orientation = "N" if lat >= 0 else "S"
        lon_orientation = "E" if lat >= 0 else "W"
        return (lat, lon, lat_orientation, lon_orientation, elevation)

    def _process_metadata_dict(self, datetime_meta: Optional[DateTime] = None) -> dict:
        """gets the labels from the the metadata segment
        and returns the output dict with correct EXIFTOOL LABELS
        works for both types of
        address metadata
        """

        def map_meta_value(fields: list) -> Optional[Any]:
            """maps fields from the dict.
            Upon first non empty occurence this value is returned"""
            for field in fields:
                value = self._meta_dict.get(field)
                if value is not None:
                    return value
            return None

        out = {}
        address_dict = self.get_value_from_meta(METADATA_SEGMENT)
        if address_dict is None:
            print(f"{C_E}🚨[GeTransformer] Couldn't find metadata segment{C_0}")
            return

        lat = None
        lon = None
        lat_orientation = None
        lon_orientation = None
        elevation = None

        gps_data = self.get_gps_data()
        if gps_data is not None:
            lat, lon, lat_orientation, lon_orientation, elevation = gps_data

        # get values from predefined metadata jsons using a mapping
        author = EXIFTOOL_AUTHOR
        authortitle = EXIFTOOL_BYLINE_TITLE

        display_name = self.get_display_name()
        geo_url = None if lat is None else Geo.latlon2osm((lat, lon))
        if datetime_meta is None:
            datetime_meta = DateTime.now()
        year = datetime_meta.strftime("%Y")
        datetime_meta_s = datetime_meta.strftime("%Y-%m-%d %H:%M:%S")
        copyright_ = f"(C) Copyright {str(year)} {EXIFTOOL_AUTHOR} "
        # IPTC Category always set to NT1 arts, culture and entertainme
        iptc_category = "NT1"
        # Urgency always set to normal
        urgency = 6
        # rating always set to 3
        rating = 3
        source = "own photography"
        rights = f"(C) {str(year)} ALL RIGHTS RESERVED"
        # misusing the genre metadata
        genre = "leisure photography"
        transmission_reference = f"Own Photography ({datetime_meta_s})"
        # filename
        filename = self._filename

        field_map = {
            # fixed values
            FILE: filename,
            AUTHOR: author,
            AUTHORTITLE: authortitle,
            SOURCE: source,
            COPYRIGHT: copyright_,
            RIGHTS: rights,
            DESCRIPTION: display_name,
            IPTC_CATEGORY: iptc_category,
            DATE_CREATED: datetime_meta_s,
            URGENCY: urgency,
            RATING: rating,
            GENRE: genre,
            ORIGINAL_TRANSMISSION_REF: transmission_reference,
            DATETIME: datetime_meta_s,
            LAT: lat,
            LON: lon,
            LAT_ORIENTATION: lat_orientation,
            LON_ORIENTATION: lon_orientation,
            ELEVATION: elevation,
            ELEVATION_REF: 1,  # elevation set to above 0 in all cases
            GEO_URL: geo_url,
            # determine
            COUNTRY: COUNTRY_LABELS,
            COUNTRY_CODE: COUNTRYCODE_LABELS,
            STATE: STATE_LABELS,
            ZIP_CODE: ZIP_LABELS,
            SUBREGION: SUBREGION_LABELS,
            LOCATION: CITY_LABELS,
        }

        for field, value in field_map.items():
            out_value = value
            # for now lists only contain field lists
            # later on we might halso consider keyword lists
            if isinstance(value, list):
                out_value = map_meta_value(value)

            if out_value is None:
                continue
            out[field] = out_value

        return out

    @staticmethod
    def _dict_key_paths(data: dict, prefix=None, name=None) -> list:
        """transforms a dict into a list of key paths"""
        if prefix is None:
            prefix = []

        paths = []
        for key, value in data.items():
            new_prefix = prefix + [key]
            if isinstance(value, dict):
                paths.extend(GeoMetaTransformer._dict_key_paths(value, new_prefix))
            else:
                paths.append(new_prefix)
        out = {"paths": paths}
        # print(f"### {name}\n{json.dumps(out, indent=4)}")

        return paths



if __name__ == "__main__":
    # just show the paths
    # GeoMetaTransformer._dict_key_paths(SAMPLE_EXIFREVERSE["sample"], name="SAMPLE_EXIFREVERSE")
    # print(list(SAMPLE_METADATA_EXIFTOOL_TAGS[0].keys()))
    pass
