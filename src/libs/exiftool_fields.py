"""Metadata structure retrieved for image files using exif tool command for cameras
exiftool -json -g -c '%.6f' *.jpg > makernotes.json
"""

import json
from typing import Optional

from config.colors import C_E

from libs.custom_print import (
    print_json,
)

# KEYS
FUJI = "FUJI"
LEICA_DLUX = "LEICA_DLUX"
MOTOROLA = "MOTOROLA"
GENERIC = "GENERIC"
UNKNOWN = "UNKNOWN"
NOT_MAPPED = "NOT MAPPED"
# Segment keys
SOURCE_FILE = "SourceFile"
EXIFTOOL = "ExifTool"
FILE = "File"
IPTC = "IPTC"
EXIF = "EXIF"
FLASHPIX = "FlashPix"
MAKERNOTES = "MakerNotes"
PRINTIM = "PrintIM"
XMP = "XMP"
MPF = "MPF"
COMPOSITE = "Composite"
IGNORE_META = ["off", "n/a", "normal", "+0"]

# Parameters to be copied into keywords field
EXIF_META_SELECTED = {
    FUJI: {
        MAKERNOTES: [
            "FilmMode",
            "GrainEffectRoughness",
            "GrainEffectSize",
            "ColorChromeEffect",
            "ColorChromeFXBlue",
            "InternalSerialNumber",
            "NoiseReduction",
            "FocusPixel",
            "FujiModel",
            "FujiModel2",
            "RollAngle",
        ]
    },
    LEICA_DLUX: {
        MAKERNOTES: [
            "PhotoStyle",
            "FilterEffect",
            "MonochromeFilterEffect",
            "MonochromeGrainEffect",
            "MacroMode",
            "ColorTempKelvin",
            "RollAngle",
            "PitchAngle",
        ]
    },
    MOTOROLA: {
        MAKERNOTES: {"BuildNumber", "CustomRendered", "DriveMode", "Sensor", "ManufactureDate"},
    },
    # NOTE NOT ALL GENERIC VALUES MIGHT BE EXISTING IN EXIF DATA FOR DIFFERENT CAMERAS
    GENERIC: {
        FILE: [
            "FileName",
            "Directory",
            "FileSize",
            "FileModifyDate",
            "FileAccessDate",
            "FileCreateDate",
            "ImageWidth",
            "ImageHeight",
            "FileType",
            "FileTypeExtension",
        ],
        IPTC: [
            "CodedCharacterSet",
            "EnvelopeRecordVersion",
            "Caption-Abstract",
            "Writer-Editor",
            "Headline",
            "SpecialInstructions",
            "By-line",
            "By-lineTitle",
            "Credit",
            "Source",
            "ObjectName",
            "DateCreated",
            "City",
            "Sub-location",
            "Province-State",
            "Country-PrimaryLocationName",
            "OriginalTransmissionReference",
            "Category",
            "SupplementalCategories",
            "Urgency",
            "Keywords",
            "CopyrightNotice",
        ],
        EXIF: [
            "ApertureValue",
            "FNumber",
            "ISO",
            "ExposureTime",
            "ExposureCompensation",
            "BrightnessValue",
            "FocalLength",
            "WhiteBalance",
            "Make",
            "Model",
            "LensMake",
            "LensModel",
            "LensInfo",
            "LensSerialNumber",
            "MaxApertureValue",
            "SerialNumber",
            "Software",
            "DateTimeOriginal",
            "CreateDate",
            "ModifyDate",
            "OffsetTime",
        ],
        COMPOSITE: [
            "Aperture",
            "ShutterSpeed",
            "ImageSize",
            "Megapixels",
            "ScaleFactor35efl",
            "CircleOfConfusion",
            "FOV",
            "FocalLength35efl",
            "HyperfocalDistance",
            "LightValue",
            "SubSecCreateDate",
            "SubSecDateTimeOriginal",
            "SubSecModifyDate",
        ],
        XMP: [
            "XMPToolkit",
            "ModifyDate",
            "MetadataDate",
            "CreatorTool",
            "Rating",
            "RatingPercent",
            "City",
            "Country",
            "AuthorsPosition",
            "Credit",
            "CaptionWriter",
            "Headline",
            "Instructions",
            "TransmissionReference",
            "State",
            "Source",
            "Category",
            "Rights",
            "Creator",
            "Description",
            "Title",
            "Subject",
            "CountryCode",
            "CreatorAddress",
            "CreatorCity",
            "CreatorCountry",
            "CreatorWorkEmail",
            "CreatorWorkTelephone",
            "CreatorPostalCode",
            "CreatorRegion",
            "CreatorWorkURL",
            "IntellectualGenre",
            "Scene",
            "SubjectCode",
            "Location",
            "DateTimeOriginal",
            "GPSLatitude",
            "GPSLongitude",
            "GPSAltitudeRef",
            "GPSAltitude",
            "UsageTerms",
            "ImageCreatorImageCreatorName",
            "LocationShownCity",
            "LocationShownCountryName",
            "LocationShownLocationName",
            "LocationShownProvinceState",
            "Orientation",
            "RawFileName",
            "AlreadyApplied",
            "HierarchicalSubject",
            "PreservedFileName",
        ],
    },
}

EXIF_META_ALL = {
    MOTOROLA: {
        MAKERNOTES: {"BuildNumber", "CustomRendered", "DriveMode", "Sensor", "ManufactureDate"},
    },
    FUJI: {
        SOURCE_FILE: [],
        EXIFTOOL: ["ExifToolVersion"],
        FILE: [
            "FileName",
            "Directory",
            "FileSize",
            "FileModifyDate",
            "FileAccessDate",
            "FileCreateDate",
            "FilePermissions",
            "FileType",
            "FileTypeExtension",
            "MIMEType",
            "ExifByteOrder",
            "ImageWidth",
            "ImageHeight",
            "EncodingProcess",
            "BitsPerSample",
            "ColorComponents",
            "YCbCrSubSampling",
        ],
        IPTC: [
            "CodedCharacterSet",
            "EnvelopeRecordVersion",
            "Caption-Abstract",
            "Writer-Editor",
            "Headline",
            "SpecialInstructions",
            "By-line",
            "By-lineTitle",
            "Credit",
            "Source",
            "ObjectName",
            "DateCreated",
            "City",
            "Sub-location",
            "Province-State",
            "Country-PrimaryLocationName",
            "OriginalTransmissionReference",
            "Category",
            "SupplementalCategories",
            "Urgency",
            "Keywords",
            "CopyrightNotice",
        ],
        EXIF: [
            "Make",
            "Model",
            "Orientation",
            "XResolution",
            "YResolution",
            "ResolutionUnit",
            "Software",
            "ModifyDate",
            "Artist",
            "YCbCrPositioning",
            "Copyright",
            "ExposureTime",
            "FNumber",
            "ExposureProgram",
            "ISO",
            "SensitivityType",
            "ExifVersion",
            "DateTimeOriginal",
            "CreateDate",
            "OffsetTime",
            "OffsetTimeOriginal",
            "OffsetTimeDigitized",
            "ComponentsConfiguration",
            "CompressedBitsPerPixel",
            "ShutterSpeedValue",
            "ApertureValue",
            "BrightnessValue",
            "ExposureCompensation",
            "MaxApertureValue",
            "MeteringMode",
            "LightSource",
            "Flash",
            "FocalLength",
            "UserComment",
            "SubSecTime",
            "SubSecTimeOriginal",
            "SubSecTimeDigitized",
            "CameraElevationAngle",
            "FlashpixVersion",
            "ColorSpace",
            "ExifImageWidth",
            "ExifImageHeight",
            "InteropIndex",
            "InteropVersion",
            "FocalPlaneXResolution",
            "FocalPlaneYResolution",
            "FocalPlaneResolutionUnit",
            "SensingMethod",
            "FileSource",
            "SceneType",
            "CustomRendered",
            "ExposureMode",
            "WhiteBalance",
            "FocalLengthIn35mmFormat",
            "SceneCaptureType",
            "Sharpness",
            "SubjectDistanceRange",
            "SerialNumber",
            "LensInfo",
            "LensMake",
            "LensModel",
            "LensSerialNumber",
            "CompositeImage",
            "Compression",
            "ThumbnailOffset",
            "ThumbnailLength",
            "ThumbnailImage",
        ],
        MAKERNOTES: [
            "Version",
            "InternalSerialNumber",
            "Quality",
            "Sharpness",
            "WhiteBalance",
            "Saturation",
            "Contrast",
            "WhiteBalanceFineTune",
            "NoiseReduction",
            "Clarity",
            "FujiFlashMode",
            "FlashExposureComp",
            "FocusMode",
            "AFMode",
            "FocusPixel",
            "AF-SPriority",
            "AF-CPriority",
            "FocusMode2",
            "PreAF",
            "AFAreaMode",
            "AFAreaPointSize",
            "AFAreaZoneSize",
            "AF-CSetting",
            "AF-CTrackingSensitivity",
            "AF-CSpeedTrackingSensitivity",
            "AF-CZoneAreaSwitching",
            "SlowSync",
            "PictureMode",
            "ExposureCount",
            "ShadowTone",
            "HighlightTone",
            "LensModulationOptimizer",
            "GrainEffectRoughness",
            "ColorChromeEffect",
            "GrainEffectSize",
            "CropMode",
            "ColorChromeFXBlue",
            "ShutterType",
            "AutoBracketing",
            "SequenceNumber",
            "DriveMode",
            "DriveSpeed",
            "BlurWarning",
            "FocusWarning",
            "ExposureWarning",
            "DynamicRange",
            "FilmMode",
            "DynamicRangeSetting",
            "DevelopmentDynamicRange",
            "MinFocalLength",
            "MaxFocalLength",
            "MaxApertureAtMinFocal",
            "MaxApertureAtMaxFocal",
            "ImageStabilization",
            "ImageGeneration",
            "ImageCount",
            "FlickerReduction",
            "FujiModel",
            "FujiModel2",
            "RollAngle",
            "FacesDetected",
            "NumFaceElements",
        ],
        PRINTIM: ["PrintIMVersion"],
        XMP: ["Rating"],
        FLASHPIX: ["PreviewImageWidth", "PreviewImageHeight", "PreviewImage"],
        COMPOSITE: [
            "Aperture",
            "ImageSize",
            "Megapixels",
            "PreviewImageSize",
            "ScaleFactor35efl",
            "ShutterSpeed",
            "SubSecCreateDate",
            "SubSecDateTimeOriginal",
            "SubSecModifyDate",
            "CircleOfConfusion",
            "FOV",
            "FocalLength35efl",
            "HyperfocalDistance",
            "LightValue",
            "LensID",
        ],
    },
    LEICA_DLUX: {
        SOURCE_FILE: [],
        EXIFTOOL: ["ExifToolVersion"],
        FILE: [
            "FileName",
            "Directory",
            "FileSize",
            "FileModifyDate",
            "FileAccessDate",
            "FileCreateDate",
            "FilePermissions",
            "FileType",
            "FileTypeExtension",
            "MIMEType",
            "ExifByteOrder",
            "ImageWidth",
            "ImageHeight",
            "EncodingProcess",
            "BitsPerSample",
            "ColorComponents",
            "YCbCrSubSampling",
        ],
        IPTC: [
            "CodedCharacterSet",
            "EnvelopeRecordVersion",
            "Caption-Abstract",
            "Writer-Editor",
            "Headline",
            "SpecialInstructions",
            "By-line",
            "By-lineTitle",
            "Credit",
            "Source",
            "ObjectName",
            "DateCreated",
            "City",
            "Sub-location",
            "Province-State",
            "Country-PrimaryLocationName",
            "OriginalTransmissionReference",
            "Category",
            "SupplementalCategories",
            "Urgency",
            "Keywords",
            "CopyrightNotice",
        ],
        EXIF: [
            "Make",
            "Model",
            "Orientation",
            "XResolution",
            "YResolution",
            "ResolutionUnit",
            "Software",
            "ModifyDate",
            "YCbCrPositioning",
            "ExposureTime",
            "FNumber",
            "ExposureProgram",
            "ISO",
            "SensitivityType",
            "StandardOutputSensitivity",
            "ExifVersion",
            "DateTimeOriginal",
            "CreateDate",
            "OffsetTime",
            "OffsetTimeOriginal",
            "OffsetTimeDigitized",
            "ComponentsConfiguration",
            "CompressedBitsPerPixel",
            "ExposureCompensation",
            "MaxApertureValue",
            "MeteringMode",
            "LightSource",
            "Flash",
            "FocalLength",
            "SubSecTime",
            "SubSecTimeOriginal",
            "SubSecTimeDigitized",
            "FlashpixVersion",
            "ColorSpace",
            "ExifImageWidth",
            "ExifImageHeight",
            "InteropIndex",
            "InteropVersion",
            "SensingMethod",
            "FileSource",
            "SceneType",
            "CustomRendered",
            "ExposureMode",
            "WhiteBalance",
            "DigitalZoomRatio",
            "FocalLengthIn35mmFormat",
            "SceneCaptureType",
            "GainControl",
            "Contrast",
            "Saturation",
            "Sharpness",
            "LensInfo",
            "LensMake",
            "LensModel",
            "LensSerialNumber",
            "Compression",
            "ThumbnailOffset",
            "ThumbnailLength",
            "ThumbnailImage",
        ],
        MAKERNOTES: [
            "ImageQuality",
            "FirmwareVersion",
            "WhiteBalance",
            "FocusMode",
            "AFAreaMode",
            "ImageStabilization",
            "MacroMode",
            "ShootingMode",
            "Audio",
            "DataDump",
            "FlashBias",
            "InternalSerialNumber",
            "PanasonicExifVersion",
            "ColorEffect",
            "TimeSincePowerOn",
            "BurstMode",
            "SequenceNumber",
            "ContrastMode",
            "NoiseReduction",
            "SelfTimer",
            "Rotation",
            "AFAssistLamp",
            "OpticalZoomMode",
            "ConversionLens",
            "TravelDay",
            "BatteryLevel",
            "Contrast",
            "WorldTimeLocation",
            "AdvancedSceneType",
            "FacesDetected",
            "Saturation",
            "Sharpness",
            "JPEGQuality",
            "ColorTempKelvin",
            "BracketSettings",
            "WBShiftAB",
            "WBShiftGM",
            "FlashCurtain",
            "LongExposureNoiseReduction",
            "PanasonicImageWidth",
            "PanasonicImageHeight",
            "AFPointPosition",
            "NumFacePositions",
            "FacesRecognized",
            "Title",
            "BabyName",
            "Location",
            "Country",
            "State",
            "City",
            "Landmark",
            "IntelligentResolution",
            "MergedImages",
            "BurstSpeed",
            "IntelligentD-Range",
            "ClearRetouch",
            "City2",
            "PhotoStyle",
            "WBShiftIntelligentAuto",
            "AccelerometerZ",
            "AccelerometerX",
            "AccelerometerY",
            "CameraOrientation",
            "RollAngle",
            "PitchAngle",
            "WBShiftCreativeControl",
            "SweepPanoramaDirection",
            "SweepPanoramaFieldOfView",
            "TimerRecording",
            "InternalNDFilter",
            "HDR",
            "ShutterType",
            "FilterEffect",
            "ClearRetouchValue",
            "TouchAE",
            "MonochromeFilterEffect",
            "HighlightShadow",
            "TimeStamp",
            "VideoBurstResolution",
            "MultiExposure",
            "RedEyeRemoval",
            "VideoBurstMode",
            "DiffractionCorrection",
            "FocusBracket",
            "LongExposureNRUsed",
            "PostFocusMerging",
            "VideoPreburst",
            "SensorType",
            "MonochromeGrainEffect",
            "TimeLapseShotNumber",
            "MakerNoteVersion",
            "SceneMode",
            "HighlightWarning",
            "DarkFocusEnvironment",
            "WBRedLevel",
            "WBGreenLevel",
            "WBBlueLevel",
            "TextStamp",
            "BabyAge",
        ],
        PRINTIM: ["PrintIMVersion"],
        XMP: ["About", "Rating"],
        MPF: [
            "MPFVersion",
            "NumberOfImages",
            "MPImageFlags",
            "MPImageFormat",
            "MPImageType",
            "MPImageLength",
            "MPImageStart",
            "DependentImage1EntryNumber",
            "DependentImage2EntryNumber",
            "PreviewImage",
        ],
        COMPOSITE: [
            "Aperture",
            "BlueBalance",
            "ImageSize",
            "Megapixels",
            "RedBalance",
            "ScaleFactor35efl",
            "ShutterSpeed",
            "SubSecCreateDate",
            "SubSecDateTimeOriginal",
            "SubSecModifyDate",
            "AdvancedSceneMode",
            "CircleOfConfusion",
            "FOV",
            "FocalLength35efl",
            "HyperfocalDistance",
            "LightValue",
        ],
    },
}

# this is a mapt that maps input fields to Image metadata for metadata changes using exiftool
MAP_METADATA: dict = {
    "file": "SourceFile",
    "author": [
        "By-line",
        "Writer-Editor",
        "Credit",
        "Contributor",
        "Creator",
        "CaptionWriter",
        "ImageCreatorImageCreatorName",
    ],
    "authortitle": ["By-lineTitle", "AuthorsPosition"],
    "source": "Source",
    "copyright": "Copyright",
    "rights": ["CopyrightNotice", "Rights", "UsageTerms"],
    "description": ["Caption-Abstract", "Headline", "ImageTitle", "Description", "Title"],
    "iptc_category": "Category",
    "make": NOT_MAPPED,
    "timezone": NOT_MAPPED,
    "date_created": "DateCreated",
    "gpsdate": "GPSDateStamp",
    "gpstime": "GPSTimeStamp",
    "gpsdatetime": "GPSDateTime",
    "urgency": "Urgency",
    "rating": "Rating",
    "genre": "IntellectualGenre",
    "original_transmission_ref": ["OriginalTransmissionReference", "TransmissionReference"],
    "datetime": NOT_MAPPED,
    "latlon": "GPSPosition",
    "lat": "GPSLatitude",
    "lon": "GPSLongitude",
    "lat_orientation": "GPSLatitudeRef",
    "lon_orientation": "GPSLongitudeRef",
    "elevation": "GPSAltitude",
    "elevation_ref": "GPSAltitudeRef",
    "heartrate": NOT_MAPPED,
    "geo_url": ["SpecialInstructions", "Instructions", "BaseURL"],
    "country": ["Country-PrimaryLocationName", "Country", "LocationShownCountryName"],
    "country_code": ["CountryCode", "Country-PrimaryLocationCode"],
    "state": ["Province-State", "State", "LocationShownProvinceState"],
    "zip_code": NOT_MAPPED,
    "subregion": "Sub-location",
    "location": ["ObjectName", "City", "Location", "LocationShownCity", "LocationShownLocationName"],
    "keywords": "Keywords",
    "software": ["CreatorTool", "Software"],
    # MOSTLY XMP Attributes that aren't mapped
    # "Subject" is a list
    # "CreatorAddress",
    # "CreatorCity",
    # "CreatorCountry",
    # "CreatorWorkEmailAddress"
    # "CreatorWorkTelephone",
    # CreatorPostalCode,
    # CreatorRegion,
    # CreatorWorkURL
    # Scene
    # SubjectCode
    # CreatorTool
    # "Software"
    # Orientation
    # "SupplementalCategories" = "xx xxx xxx"
    # HierarchicalSubject
    # ObjectAttributeReference > Intellectual Genre
    # "Orientation"
}


class ExifToolFieldsMapper:
    """class to parse image meta data and to export keywords, etc"""

    def __init__(
        self,
        metadata: dict,
        transformed_metadata: Optional[dict] = None,
        lensinfo: Optional[str] = None,
    ):
        """uses preprocessed data to parse keywords"""
        self._metadata: dict = metadata
        self._metadata_file: dict = metadata.get(FILE, {})
        self._metadata_iptc: dict = metadata.get(IPTC, {})
        self._metadata_exif: dict = metadata.get(EXIF, {})
        self._metadata_composite: dict = metadata.get(COMPOSITE, {})
        self._metadata_makernotes: dict = metadata.get(MAKERNOTES, {})
        self._make = self._metadata_exif.get("Make", UNKNOWN).lower()
        # output of GeoMetaTransformer
        self._transformed_metadata: Optional[dict] = (
            transformed_metadata if isinstance(transformed_metadata, dict) else {}
        )
        # get the camera type
        if "fuji" in self._make:
            self._make = FUJI
        elif "leica" in self._make:  #
            self._make = LEICA_DLUX  # enough for my use case
        elif MOTOROLA in self._make:
            self._make = MOTOROLA
        # override any lens infos / might be useful when other manual lenses are used not covered here
        self._lensinfo: Optional[str] = lensinfo

    def get_camera_info(self) -> str:
        """determines the camera string"""
        make = self._metadata_exif.get("Make", "unknown").strip()
        model = self._metadata_exif.get("Model", "").strip()

        if self._make == LEICA_DLUX:
            # for leica make and model are redundantly used
            return f"{model}"
        else:
            return (f"{make} {model}").strip()

    def _get_lens_info_fuji(self) -> str:
        """For manual lenses FUJI offers settings in menu
        Enable recording w/o lens: Cog Wheel  > Key/Dial Setting  > 2 > Record w/o Lens
        Define a manual lens with focal length: IQ Menu > 4 > Adapter settings > Lens Input
        Following etnries can be found in EXIF Data / example
        [EXIF]
        FocalLength: 22.0 mm
        LensInfo: 22mm f/?"
        LensMake: ""
        LensModel: LENSBABY 22 <- this is the lens name entered manually into camera
        [MAKERNOTES]
        MinFocalLength: 22,
        MaxFocalLength: 22,
        For autiomaitc lenses this would sth. like this
        LensInfo: 28mm f/4.5
        LensMake: VILTROX
        LensModel: AF 28/4.5 XF
        """
        # TODO Refactor / List of curated manual lenses (right now there's only one 🤡)
        manual_lenses = {"LENSBABY22": "Lensbaby Sweet 22 F/3.5"}
        lens_model = self._metadata_exif.get("LensModel", "")
        lens_info = self._metadata_exif.get("LensInfo", "unknown")
        lens_make = self._metadata_exif.get("LensMake", "")
        # unknown lens manufacturer
        if len(lens_make) == "":
            lens_model = lens_model.lower()
            # lensbaby used as lens name or 22mm used as focal length
            if "lensbaby" in lens_model or "22" in lens_info:
                return manual_lenses["LENSBABY22"]
        return f"{lens_make.strip()} {lens_model}"

    def _get_lens_info_dlux(self) -> str:
        """Leica DLUX Maker Infos / doesn't work for interchangeable cameras
        "Model": "LEICA D-Lux 8",
        LensInfo": 10.9-34mm f/1.7-2.8"
        LensMake": LEICA CAMERA AG"
        LensModel": DC VARIO-SUMMILUX 1:1.7-2.8/10.9-34 ASPH.
        """
        lens_model = self._metadata_exif.get("Model", "")
        lens_info = self._metadata_exif.get("LensInfo", "unknown")
        return f"{lens_model.strip()} {lens_info}"

    def _get_lens_info_motorola(self) -> str:
        """Motorola Metadata
        [EXIF]
        "Make": "motorola",
        "Model": "motorola edge 40 neo",
        "DigitalZoomRatio": 1,
        "FocalLength": "5.6 mm",
        """
        model = self._metadata_exif.get("Model", "unknown")
        focal_length = self._metadata_exif.get("FocalLength", "unknown")
        zoom = float(self._metadata_exif.get("DigitalZoomRatio", "1"))
        zoom = "" if zoom == "1.0" else f" (zoom {str(round(zoom, 1))})"
        return f"{model} {focal_length}{zoom}"

    def _get_lens_info(self) -> str:
        """gets the lens model"""

        # override in any case if lens is submitted
        if self._lensinfo is not None:
            return self._lensinfo

        if self._make == FUJI:
            return self._get_lens_info_fuji()
        elif self._make == LEICA_DLUX:
            return self._get_lens_info_dlux()
        elif self._make == MOTOROLA:
            return self._get_lens_info_motorola()
        else:
            lens_make: str = self._metadata_exif.get("LensMake", "").strip()
            lens_model: str = self._metadata_exif.get("LensModel", "unknown").strip()
            return (f"{lens_make} {lens_model}").strip()

    def _get_shot_info(self) -> list[str]:
        """get classic image params ISO,f,F, ..."""
        out = []

        attributes_composite = [
            "ScaleFactor35efl",
            "Aperture",
            "Megapixels",
            "LightValue",
            "CircleOfConfusion",
            "FOV",
            "HyperfocalDistance",
        ]

        attributes_dict = {
            attribute: self._metadata_composite.get(attribute)
            for attribute in attributes_composite
            if self._metadata_composite.get(attribute) is not None
        }

        attributes_exif = [
            "ISO",
            "ExposureTime",
            "FocalLength",
            "FocalLengthIn35mmFormat",
            "ExposureCompensation",
            "Orientation",
            "Contrast",
            "Saturation",
            "Sharpness",
        ]

        exif_dict = {
            attribute: self._metadata_exif.get(attribute)
            for attribute in attributes_exif
            if self._metadata_exif.get(attribute) is not None
        }

        attributes_dict.update(exif_dict)

        # mapping metadata attributes to keyvalue attributes
        # add items her so that they will be added to metadata
        attribute_text_map = {
            "FocalLength": "f",  # 33.0 mm
            "FocalLengthIn35mmFormat": "f(FullFrame)",  # 50 mm
            "FOV": "FoV",  # 38.9 deg
            "ExposureTime": "T",  # "1/900
            "Aperture": "F",  # 2.7
            "ISO": "ISO",  # 125
            "LightValue": "EV",  # 6.8
            "ExposureCompensation": "",
            "Contrast": "",
            "Saturation": "",
            "Sharpness": "",
            "ScaleFactor35efl": "Crop",  # 2.2
            "Megapixels": "MPix",  # 16.8
            "CircleOfConfusion": "coc",  # 0.014 mm"
            "HyperfocalDistance": "hfD",  # 14.46 m
            "Orientation": "",
        }

        # used units in metadata
        # units = ["mm", "m", "deg"]

        # ignore items
        ignore_words = ["normal", "unknown", "n/a", "off", "auto"]

        # now create keywords if existent
        for attribute, attribute_text in attribute_text_map.items():
            attribute_text_ = attribute_text if attribute_text != "" else attribute
            value = attributes_dict.get(attribute)
            if value is None:
                continue
            if not isinstance(value, str):
                value = str(value)

            if len(value) == 0:
                continue

            # ignore items with values to be ignored
            if len([iw for iw in ignore_words if iw in value.lower()]) > 0:
                continue

            # special case convert coc to um
            if attribute == "CircleOfConfusion":
                value = int(1000 * float(value.split()[0]))
                value = f"{str(value)}um"
            elif attribute == "ExposureTime":
                value = f"{value}s"
            elif attribute == "Megapixels":
                value = f"{value}MP"
            elif attribute in ["FOV", "FocalLength", "FocalLengthIn35mmFormat"]:
                if attribute == "FOV":
                    unit = "deg"
                    value_ = value.replace("deg", "")
                else:
                    unit = "mm"
                    value_ = value.replace("mm", "")
                try:
                    value_ = float(value_)
                    value = str(int(round(value_, 0))) + unit
                except (IndexError, ValueError, AttributeError):
                    pass

            # drop all spaces
            value = value.replace(" ", "")
            out.append(f"{attribute_text_} {value}")
        return out

    def _get_metadata(self, metadata: dict, attributes: list[str]) -> dict:
        """creates the list of makernote attributes"""
        out = {}
        for attribute in attributes:
            value = metadata.get(attribute)
            if value is None:
                continue
            # check if all items are normal
            num_ignore = len([im for im in IGNORE_META if im in str(value).lower()])

            if num_ignore > 0:
                continue
            out[attribute] = f"{attribute} {str(value)}"
        return out

    def _get_makernotes_fuji(self) -> list[str]:
        """return camera specific maker notes for FUJI"""

        attributes = [
            "FilmMode",
            "ColorChromeEffect",
            "ColorChromeFXBlue",
            "GrainEffectRoughness",
            "GrainEffectSize",
            "Contrast",
            "Saturation",
            "Clarity",
            "WhiteBalanceFineTune",
            "RollAngle",
            "ImageCount",
        ]

        makernotes = list(self._get_metadata(self._metadata_makernotes, attributes).values())
        return makernotes

    def _get_makernotes_dlux(self) -> list[str]:
        """return camera specific maker notes for DLUX"""

        attributes = [
            "PhotoStyle",
            "FilterEffect",
            "ColorEffect",
            "MonochromeFilterEffect",
            "MonochromeGrainEffect",
            "SceneMode",
            "ColorTempKelvin",
            "AFPointPosition",
            "FilterEffect",
            "",
            "Rotation",
            "RollAngle",
            "PitchAngle",
            "WBShiftAB",
            "WBShiftGM",
            "WBRedLevel",
            "WBGreenLevel",
            "WBBlueLevel",
        ]

        makernotes = list(self._get_metadata(self._metadata_makernotes, attributes).values())
        return makernotes

    def _get_iptc_metadata(self) -> list[str]:
        """get any existing IPTC makernotes"""
        out = []
        attributes: dict = {
            "ObjectName": "Geo-Object",
            "City": "Geo-City",
            "Sub-location": "Geo-Location",
            "Province-State": "Geo-State",
            "Country-PrimaryLocationName": "Geo-Country",
        }

        mapped_attributes: dict[str, str] = self._get_metadata(self._metadata_iptc, list(attributes.keys()))
        # remap the key values to be used in Keywords list
        for attribute, mapped_value in mapped_attributes.items():
            out.append(mapped_value.replace(attribute, attributes[attribute]))
        return out

    def _get_transformed_metadata(self) -> list[str]:
        """get any extra tramsformed exif metadata
        output similar to:
        {
            "file": "test.jpg",
            "author": "UNKNOWNN AUTHOR",
            "authortitle": "Honorable",
            "source": "own photography",
            "copyright": "(C) Copyright 2025 UNKNOWNN AUTHOR ",
            "rights": "(C) 2025 ALL RIGHTS RESERVED",
            "description": "Weiherstraße, Bahnbrücken, Kraichtal, Landkreis Karlsruhe, Baden-Württemberg, 76703, Deutschland",
            "iptc_category": "NT1",
            "timezone": "Europe/Berlin",
            "date_created": "2025-08-31 14:34:46",
            "urgency": 6,
            "rating": 3,
            "genre": "leisure photography",
            "original_transmission_ref": "Own Photography (2025-08-31 14:34:46)",
            "datetime": "2025-08-31 14:34:46",
            "latlon": "49.119324N_8.79133E (242m)",
            "lat": 49.119324,
            "lon": 8.79133,
            "lat_orientation": "N",
            "lon_orientation": "E",
            "elevation": 242,
            "elevation_ref": 1,
            "heartrate": 136,
            "geo_url": "https://www.openstreetmap.org/#map=18/49.119324/8.79133",
            "country": "Deutschland",
            "country_code": "de",
            "state": "Baden-Württemberg",
            "zip_code": "76703",
            "subregion": "Kraichtal",
            "location": "Bahnbrücken"
        }
        """
        out = []

        # map alongside with unit information
        attributes: dict = {
            "country_code": ("Geo-CountryCode", ""),
            "latlon": ("Geo-Coordinates", ""),
            "elevation": ("Geo-Height", "m"),
            "zip_code": ("Geo-ZipCode", ""),
            "timezone": ("Geo-Timezone", ""),
            "temperature": ("Geo-Temperature", "°C"),
            "heartrate": ("Heartrate", "bpm"),
        }

        for attribute, keyword in attributes.items():
            value = self._transformed_metadata.get(attribute)
            if value is None:
                continue
            out.append(f"{keyword[0]} {value}{keyword[1]}")

        return out

    def _get_makernotes_keywords(self) -> list[str]:
        """return camera specific maker notes as keywords"""
        if self._make == FUJI:
            return self._get_makernotes_fuji()
        elif self._make == LEICA_DLUX:
            return self._get_makernotes_dlux()
        return []

    def get_keywords(self) -> list[str]:
        """get list of keywords as per submitted metadata"""
        # camera metadata
        out = [self.get_camera_info(), self._get_lens_info()]
        # iptc data / geodata if existent
        out.extend(self._get_iptc_metadata())
        # trnasformed metadata
        out.extend(self._get_transformed_metadata())
        # camera settings
        out.extend(self._get_shot_info())
        # camera makernotes
        out.extend(self._get_makernotes_keywords())
        # clean up keywords
        out = [meta.strip() if isinstance(meta, str) else meta for meta in out]
        return out

    @staticmethod
    def get_valid_exiftool_attributes() -> list[str]:
        """returns a list of valid metadata"""
        metadata_values = list(MAP_METADATA.values())
        out = []
        for metadata in metadata_values:
            if isinstance(metadata, list):
                out.extend(metadata)
                continue
            if metadata == NOT_MAPPED:
                continue
            out.append(metadata)

        return out

    def map_metadata(self, metadata: dict) -> dict:
        """Map all found metadtata into a dict to be used for exiftool update"""
        # we collect all listed fields for validation
        out: dict = {}
        valid_metadata = []
        invalid_metadata = []

        # valid_metadata = tuple(list(MAP_METADATA.keys()))
        exiftool_attributes_valid = ExifToolFieldsMapper.get_valid_exiftool_attributes()

        # map any input attributes to valid exiftooll attributes
        for attribute, value in metadata.items():
            exiftool_attributes = attribute
            if attribute not in exiftool_attributes_valid:
                exiftool_attributes = MAP_METADATA.get(attribute)

            # couldn't find any valid mapping
            if exiftool_attributes is None:
                invalid_metadata.append(attribute)
                continue

            if isinstance(exiftool_attributes, str):
                exiftool_attributes = [exiftool_attributes]

            for exiftool_attribute in exiftool_attributes:
                valid_metadata.append(attribute)
                if exiftool_attribute == NOT_MAPPED:
                    continue
                # do not update if the value was set before
                original_value = metadata.get(exiftool_attribute)
                out[exiftool_attribute] = original_value if original_value is not None else value

        print_json(
            out,
            f"[ExifToolsFieldMapper] Valid Update Keywords for [{out.get('FileName')}]",
            True,
            "DEBUG",
        )

        if len(invalid_metadata) > 0:
            print_json(
                {"make": self._make, "invalid": invalid_metadata},
                f"[ExifToolsFieldMapper] Invalid Update Keywords for [{out.get('FileName')}]",
                True,
                "DEBUG",
                C_E,
            )

        return out


# Example usage:
if __name__ == "__main__":
    pass
