"""Binary Sort on Dicts"""

from typing import Dict, List, Any
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F, C_W


class BinarySorter:
    """Class for Binary Sorting, right now for numerical values only"""

    def __init__(
        self,
        items: Dict | List,
        sort_key: str = None,
        key_as_sortvalue: bool = False,
    ):
        """Constructor"""
        self._original: Dict | List = items
        self._index: Dict[Any, Any] = {}

        self._max_index: int = 0
        self._current_index: int = None
        self._sort_key: str = sort_key
        self._key_as_sortvalue: bool = key_as_sortvalue
        self._data: Dict[Any, Any] = {}

        # get data from a dict
        if isinstance(items, List):
            self._data = {i: data for i, data in enumerate(items, 1)}
        else:
            self._data = items

    def _create_index(self):
        """creates the sort index"""
        self._index = {}
        for idx, (k, v) in enumerate(self._data.items()):
            _index_value = None
            _index_key = k
            if self._key_as_sortvalue:
                _index_value = k
            else:
                _index_value = v.get(self._sort_key)

            if not _index_value:
                print(f"{C_E}No sort key [{self._sort_key}] found in [{k}/{v}] {C_0}")
                continue
            self._index[_index_value] = _index_key
        # now sort
        self._index = dict(sorted(self._index.items()))
        pass
