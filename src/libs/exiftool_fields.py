"""Metadata structure retrieved for image files using exif tool command for cameras
exiftool -json -g -c '%.6f' *.jpg > makernotes.json
"""

from typing import Optional

# KEYS
FUJI = "FUJI"
LEICA = "LEICA_DLUX"
GENERIC = "GENERIC"
# Segment keys
SOURCE_FILE = "SourceFile"
EXIFTOOL = "ExifTool"
FILE = "File"
IPTC = "EXIF"
EXIF = "EXIF"
FLASHPIX = "FlashPix"
MAKERNOTES = "MakerNotes"
PRINTIM = "PrintIM"
XMP = "XMP"
MPF = "MPF"
COMPOSITE = "Composite"
IGNORE_META = ["off", "n/a", "normal"]

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
    LEICA: {
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
    },
}

EXIF_META_ALL = {
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
    LEICA: {
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


class ExifToolFieldsMapper:
    """class to parse image meta data and to export keywords, etc"""

    def __init__(self, metadata: dict):
        self._metadata: dict = metadata
        self._metadata_file: dict = metadata.get(FILE, {})
        self._metadata_iptc: dict = metadata.get(IPTC, {})
        self._metadata_exif: dict = metadata.get(EXIF, {})
        self._metadata_composite: dict = metadata.get(COMPOSITE, {})
        self._metadata_makernotes: dict = metadata.get(MAKERNOTES, {})
        self._camera = self._metadata_exif.get("Make", "na").lower()
        # get the camer tyoe
        if "fuji" in self._camera:
            self._camera = FUJI
        elif "leica" in self._camera:
            self._camera = LEICA

    def _get_camera_info(self) -> str:
        """determines the camera string"""
        make = self._metadata_exif.get("Make")
        model = self._metadata_exif.get("Model")
        if self._camera == FUJI:
            return f"{make} {model}"
        if self._camera == LEICA:
            # for leica we make and model are redundantly used
            return f"{model}"
        return "unknown camera"

    def _get_lens_info(self) -> str:
        """gets the lens model"""
        # only het the first part
        lensmake: str = (self._metadata_exif.get("LensMake", "unknown_lens").split()[0]).strip()
        lensinfo: str = (self._metadata_exif.get("LensInfo", "lensinfo")).strip()
        return f"{lensmake} {lensinfo}"

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

        attributes_exif = ["ISO", "ExposureTime", "FocalLength", "FocalLengthIn35mmFormat"]

        exif_dict = {
            attribute: self._metadata_exif.get(attribute)
            for attribute in attributes_exif
            if self._metadata_exif.get(attribute) is not None
        }

        attributes_dict.update(exif_dict)

        attributes_numerical = ["ScaleFactor35efl", "Aperture", "Megapixels", "LightValue", "ISO"]
        # mapping metadata attributes to keyvalue attributes
        attribute_text_map = {
            "FocalLength": "f",  # 33.0 mm
            "FocalLengthIn35mmFormat": "f(FullFrame)",  # 50 mm
            "FOV": "FoV",  # 38.9 deg
            "ExposureTime": "T",  # "1/900
            "Aperture": "F",  # 2.7
            "ISO": "ISO",  # 125
            "LightValue": "EV",  # 6.8
            "ScaleFactor35efl": "Crop",  # 2.2
            "Megapixels": "MPix",  # 16.8
            "CircleOfConfusion": "coc",  # 0.014 mm"
            "HyperfocalDistance": "hfD",  # 14.46 m
        }

        # used units in metadata
        units = ["mm", "m", "deg"]

        # now create keywords if existent
        for attribute, attribute_text in attribute_text_map.items():
            value = attributes_dict.get(attribute)
            if value is None:
                continue
            if attribute in attributes_numerical:
                value = str(value)
            # special case convert coc to um
            if attribute == "CircleOfConfusion":
                value = round(1000 * float(value.split()[0]), 0)
                value = f"str({value})um"

            # drop all spaces
            value = value.replace(" ", "")
            out.append(f"{attribute_text} {value}")
        return out

    def _get_makernotes(self, makernotes: dict, attributes: list[str]) -> dict:
        """creates the list of makernote attributes"""
        out = {}
        for attribute in attributes:
            value = makernotes.get(attribute)
            if value is None:
                continue
            # check if all items are normal
            num_ignore = len([im for im in IGNORE_META if im in attribute.lower()])
            if num_ignore > 0:
                continue
            out[attribute] = f"{attribute} ({str(value)})"
        return out

    def _get_makernotes_fuji(self) -> list[str]:
        """return camera specific maker notes for FUJI"""

        attributes = [
            "FilmMode",
            "ColorChromeEffect",
            "ColorChromeFXBlue",
            "GrainEffectRoughness",
            "GrainEffectSize",
            "ImageCount",
        ]

        return list(self._get_makernotes(self._metadata_makernotes, attributes).values())

    def _get_makernotes_leica(self) -> list[str]:
        """return camera specific maker notes for FUJI"""
        attributes = [
            "PhotoStyle",
            "FilterEffect",
            "MonochromeFilterEffect",
            "MonochromeGrainEffect",
            "SceneMode",
            "ColorTempKelvin",
            "AFPointPosition",
            "FilterEffect",
        ]

        return list(self._get_makernotes(self._metadata_makernotes, attributes).values())

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

        mapped_attributes: dict[str, str] = self._get_makernotes(self._metadata_iptc, list(attributes.keys()))
        # remap the key values to be used in Keywords list
        for attribute, mapped_value in mapped_attributes.items():
            out.append(mapped_value.replace(attribute, attributes[attribute]))
        return out

    def _get_makernotes_keywords(self) -> list[str]:
        """return camera specific maker notes as keywords"""
        if self._camera == FUJI:
            return self._get_makernotes_fuji()
        elif self._camera == LEICA:
            return self._get_makernotes_leica()
        return []

    def get_keywords(self) -> list[str]:
        """get list of keywords as per submitted metadata"""
        # camera metadata
        out = [self._get_camera_info(), self._get_lens_info]
        # camera settings
        out.extend(self._get_shot_info())
        # camera makernotes
        out.extend(self._get_makernotes_keywords())
        # iptc data / geodata if existent
        out.extend(self._get_iptc_metadata())
        return out


# Example usage:
if __name__ == "__main__":
    pass
