"""Just Constant Definitions distrbuted across modules."""

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
FILES_ENV = "files_env"
METADATA_EXIF = "metadata_exif"
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
GPS_METADATA = "gps_metadata"
TIMESTAMP_UTC = "timestamp_utc"
TIMEZONE = "timezone"
TIMEZONE_DEFAULT = "Europe/Berlin"
# etxra gps data
ELEVATION = "elevation"
HEARTRATE = "heartrate"

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
F_TIMESTAMP_IMG_ENV = "timestamp_img.env"
F_TIMESTAMP_GPS = "timestamp_gps.json"
F_TIMESTAMP_CAMERA = "timestamp_camera.json"

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
