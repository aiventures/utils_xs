"""Does a reverse Geo LookUp
https://nominatim.org/release-docs/latest/api/Overview/
Usage Policy: https://operations.osmfoundation.org/policies/nominatim/
"""

import requests
from typing import Tuple, Dict, List
from datetime import datetime as DateTime
import time
import json
from copy import deepcopy
from config.local_config import NOMINATIM_USER_AGENT
from pathlib import Path
from libs.helper import Persistence
import os

# ANSI color codes
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F, C_W, C_S
from config.constants import REVERSE_GEO_INFO, EXTERNAL_KEY_MAP, EXTRA


class ReverseGeo:
    def __init__(
        self,
        user_agent: str = NOMINATIM_USER_AGENT,
        language: str = "de",
        format_: str = "jsonv2",
        zoom: int = 17,
        f_reverse_geo: str = None,
        load: bool = True,
    ):
        """Constructor"""
        # buffer past requests for this instance
        # It's a dictionary of past lat lon queries
        self._reverse_geo_info: Dict = {}
        self._headers: Dict = {"User-Agent": user_agent, "Accept-Language": language}
        self._zoom = zoom
        self._params: Dict = {"lat": None, "lon": None, "format": format_, "addressdetails": 1, "zoom": zoom}
        self._url: str = "https://nominatim.openstreetmap.org/reverse"
        _p_save = None if f_reverse_geo is None else Path(f_reverse_geo).parent.is_dir()
        self._f_reverse_geo: Path = Path(f_reverse_geo) if _p_save else None
        self._waittime: float = 1.5
        self._extkey_map: Dict = {}
        # load the date upon instanciation
        if load:
            self.load()

    def read_geo_info(
        self, lat_lon: Tuple | Dict, ext_key: str = None, add_text: str = None, extra: dict = None
    ) -> Dict:
        """Gets the reverse Geo Coordinates, optionally using external key"""
        _add_text = "" if add_text is None else add_text
        reverse_geo = None

        lat, lon = lat_lon
        lat = round(float(lat), 5)
        lon = round(float(lon), 5)
        lat_s = str(lat).replace(".", "_")
        lon_s = str(lon).replace(".", "_")
        key = f"{lat_s}-{lon_s}"
        self._params["lat"] = lat
        self._params["lon"] = lon
        osm_link = f"https://www.openstreetmap.org/#map={self._zoom}/{lat}/{lon}"

        # try if it's in buffer already
        reverse_geo = self._reverse_geo_info.get(key)
        _ext_key_str = "" if ext_key is None else f"[{ext_key}]"
        if reverse_geo:
            if ext_key:
                self._extkey_map[ext_key] = key
            print(
                f"{C_H}🔢 [ReverseGeo] 📙 Read {_ext_key_str} from Buffer, coordinates 🌍 {C_PY}{lat_lon} {_add_text}{C_0}"
            )
            print(f"{C_I}                🎯 {reverse_geo.get('display_name', 'not found')}{C_0}")
            print(f"{C_PY}                🌍 {osm_link}{C_0}")

            return reverse_geo
        try:
            print(
                f"{C_H}🔢 [ReverseGeo] 📙 Read {_ext_key_str} from Service, coordinates 🌍 {C_PY}{lat_lon} {_add_text}{C_0}"
            )
            response = requests.get(self._url, params=self._params, headers=self._headers, timeout=10)
            response.raise_for_status()
            # Decode response text as UTF-8 and parse JSON
            reverse_geo = json.loads(response.text.encode("utf-8").decode("utf-8"))
            self._reverse_geo_info[key] = reverse_geo
            # map the ext key to internal key
            if ext_key:
                self._extkey_map[ext_key] = key
            if extra:
                reverse_geo[EXTRA] = extra
            print(f"{C_I}                🎯 {reverse_geo.get('display_name', 'not found')}{C_0}")
            print(f"{C_PY}                🌍 {osm_link}{C_0}")

            # throttle the request time
            time.sleep(self._waittime)
            return reverse_geo
        except requests.RequestException as e:
            print(f"{C_E}🚨 [ReverseGeo] Error Occured for getting {lat_lon} {C_0}")
            return {"error": str(e)}

    def delete(self):
        """Deletes the file if present"""
        if self._f_reverse_geo and self._f_reverse_geo.is_file():
            print(f"{C_W}🚮 [ReverseGeo] Delete Reverse Geo {C_F}[{self._f_reverse_geo}]{C_0}")
            os.remove(str(self._f_reverse_geo))

    def save(self):
        """saves the reverse metadata buffers"""
        if self._f_reverse_geo is None:
            print(f"{C_E}🚨 [ReverseGeo] No valid file reference, no saving will be done {C_0}")
            return
        out = {REVERSE_GEO_INFO: self._reverse_geo_info, EXTERNAL_KEY_MAP: self._extkey_map}
        Persistence.save_json(self._f_reverse_geo, out)

    def load(self):
        """loads the referenced file"""
        _data = None
        if self._f_reverse_geo and self._f_reverse_geo.is_file():
            _data = Persistence.read_json(self._f_reverse_geo)
        if _data is None:
            print(f"{C_W}🚨 [ReverseGeo] No data were loaded{C_0}")
            return
        print(f"{C_H}🔢 [ReverseGeo] Read data from {str(self._f_reverse_geo)}{C_0}")
        self._extkey_map = _data.get(EXTERNAL_KEY_MAP, {})
        self._reverse_geo_info = _data.get(REVERSE_GEO_INFO)

    def get_geo_info_dict(self, as_ext_key: bool = False):
        """returns the buffered requests"""
        out = {}
        _key_map = self._extkey_map
        if as_ext_key is False:
            _keys = list(self._reverse_geo_info.keys())
            _key_map = {_key: _key for _key in _keys}
        for _key, _value in _key_map.items():
            out[_key] = self._reverse_geo_info[_value]
        return out


# Example usage:
if __name__ == "__main__":
    reverse_geo = ReverseGeo()
    coords = (49.121551, 8.788664)
    metadata = reverse_geo.read_geo_info(coords)
    print(json.dumps(metadata, indent=4))
    metadata = reverse_geo.read_geo_info(coords)
