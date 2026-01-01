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
EXIF = "EXIF"
FLASHPIX = "FlashPix"
MAKERNOTES = "MakerNotes"
PRINTIM = "PrintIM"
XMP = "XMP"
MPF = "MPF"
COMPOSITE = "Composite"

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
        self._metadata_exif: dict = metadata.get(EXIF, {})
        self._metadata_composite: dict = metadata.get(COMPOSITE, {})
        self._metadata_makernotes: dict = metadata.get(MAKERNOTES, {})
        self._camera = self._metadata_exif.get("Make", "na").lower()
        # get the camer tyoe
        if "fuji" in self._camera:
            self._camera = FUJI
        elif "leica" in self._camera:
            self._camera = LEICA

    def _get_camera(self) -> str:
        """determines the camera string"""
        make = self._metadata_exif.get("Make")
        model = self._metadata_exif.get("Model")
        if self._camera == FUJI:
            return f"{make} {model}"
        if self._camera == LEICA:
            # for leica we make and model are redundantly used
            return f"{model}"
        return "unknown"

    def _get_lens(self) -> str:
        """gets the lens model"""
        # only het the first part
        lensmake: str = (self._metadata_exif.get("LensMake", "unknown").split()[0]).strip()
        lensinfo: str = (self._metadata_exif.get("LensInfo", "unknown")).strip()
        return f"{lensmake} {lensinfo}"

    def _get_shot_info(self) -> list[str]:
        """get classic image params ISO,f,F, ..."""
        out = []

        ### COMPOSITE INFO

        # float values
        crop_factor: Optional[float] = str(self._metadata_composite.get("ScaleFactor35efl"))
        crop_factor_s = f"crop {str(crop_factor)}"
        aperture: Optional[float] = str(self._metadata_composite.get("Aperture"))
        aperture_s = f"F{str(aperture)}"

        mp: Optional[float] = round(self._metadata_composite.get("Megapixels", 0.0), 1)
        mp_s = f"{str(mp)}MPix"
        lv: Optional[float] = round(self._metadata_composite.get("LightValue", 0.0), 1)
        lv_s = f"{str(lv)}EV"

        # string values
        # circle of confusion in micrometers
        coc: Optional[float] = int(1000 * float((self._metadata_composite.get("CircleOfConfusion", 0.0)).split()[0]))
        coc_s = f"coc {str(coc)}um"
        fov: Optional[float] = round(float(self._metadata_composite.get("FOV", "0.0").split()[0]), 0)  # field of view
        fov_s = f"fov {str(fov)}deg"
        hfd: Optional[str] = (self._metadata_composite.get("HyperfocalDistance", "NA")).replace(" ", "")
        hfd_s = f"hyperfocal {hfd}"

        ### EXIF INFO
        f_number: Optional[float] = round(self._metadata_exif.get("FNumber", 0.0), 1)
        f_number_s = f"F{str(fov)}"

        iso: Optional[float] = round(self._metadata_exif.get("ISO", 0.0), 0)
        iso_s = f"ISO{str(iso)}"
        exposure_time: Optional[str] = self._metadata_exif.get("ExposureTime", "") + "s"
        focal_length: Optional[str] = self._metadata_exif.get("FocalLength", "NA").replace(" ", "")
        focal_length_s = "f{focal_length}"
        focal_length_35mm: Optional[str] = self._metadata_exif.get("FocalLengthIn35mmFormat", "NA").replace(" ", "")
        focal_length_35mm_s = "f{focal_length} FullFrame"
        return out

    def _get_maker_info_fuji(self) -> list[str]:
        """return camera specific maker notes for FUJI"""
        out = []
        # TODO IMPLEMENT
        return out

    def _get_maker_info_leica(self) -> list[str]:
        """return camera specific maker notes for FUJI"""
        out = []
        # TODO IMPLEMENT

        return out

    def _get_maker_info(self) -> list[str]:
        """return camera specific maker notes"""
        if self._camera == FUJI:
            return self._get_maker_info_fuji()
        elif self._camera == LEICA:
            return self._get_maker_info_leica()
        return []


# Example usage:
if __name__ == "__main__":
    pass
