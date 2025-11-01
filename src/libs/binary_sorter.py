"""Binary Sort on Dicts"""

import time
from typing import Dict, List, Any, Tuple
from config.colors import C_0, C_E, C_Q, C_I, C_T, C_PY, C_P, C_H, C_B, C_F, C_W


class BinarySorter:
    """Class for Binary Sorting, right now for numerical values only"""

    def __init__(
        self, items: Dict | List, sort_key: str = None, key_as_sortvalue: bool = False, sequential_search: int = 0
    ):
        """Constructor"""
        self._original: Dict | List = items
        self._index: Dict[Any, Any] = {}

        self._max_index: int = 0
        self._current_index: int = None
        self._sort_key: str = sort_key
        self._key_as_sortvalue: bool = key_as_sortvalue
        self._data: Dict[Any, Any] = {}
        self._key_values: list = None
        self._current_index: float | int = None
        self._sequential_search: int = sequential_search

        # get data from a dict
        if isinstance(items, List):
            self._data = {i: data for i, data in enumerate(items)}
        else:
            self._data = items
        self._create_index()
        self._count = len(self._key_values)
        # number of items for sequential search
        self._index_range = max(1, ((sequential_search * self._count) // 100))
        if sequential_search == 0:
            self._index_range = 0

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

            if _index_value is None:
                print(f"{C_E}No sort key [{self._sort_key}] found in [{k}/{v}] {C_0}")
                continue
            self._index[_index_value] = _index_key
        # now sort
        self._index = dict(sorted(self._index.items()))
        self._key_values = list(self._index.keys())

    def _linear_vicinity_search(self, target_value: float | int) -> Any:
        """
        Attempts a linear search in the vicinity above the current index.

        Parameters:
            target_value (float | int): The value to search for.
            window_percent (float): Fraction of total index to scan forward (e.g., 0.1 = 10%).

        Returns:
            Any: Matching value from self._index if found, else None.
        """
        if self._current_index is None:
            return None

        if self._index_range == 0:
            return None

        start_idx = self._current_index
        end_idx = min(start_idx + self._index_range, self._count)

        best_key = None
        min_diff = float("inf")

        for i in range(start_idx, end_idx):
            key = self._key_values[i]
            diff = abs(key - target_value)
            if diff < min_diff:
                min_diff = diff
                best_key = key

        if best_key is not None and min_diff < abs(self._key_values[start_idx] - target_value):
            self._current_index = self._key_values.index(best_key)
            return self._index[best_key]

        return None

    def search(self, target_value: float | int) -> Any:
        """
        Finds the value in self._index whose key is numerically closest to the given target.

        Optimized for sequentially increasing target values by storing the last successful
        index position. If a lower target is passed, the search resets to the full range.

        Parameters:
            target (float | int): The numerical value to search for.

        Returns:
            Any: The value associated with the closest key in self._index.
                Returns None if the index is empty.
        """
        if not self._index:
            print(f"{C_E}Index is empty. Did you run _create_index()?{C_0}")
            return None

        # Edge cases: outside bounds
        if target_value < self._key_values[0]:
            self._current_index = 0
            print(f"{C_W} Value [{target_value}] is below first element [{self._key_values[0]}]{C_0}")
            return None

        if target_value > self._key_values[-1]:
            self._current_index = len(self._key_values) - 1
            print(f"{C_W} Value [{target_value}] is above last element [{self._key_values[-1]}]{C_0}")
            return None

        # Exact match at boundaries
        if target_value == self._key_values[0]:
            self._current_index = 0
            return self._index[self._key_values[0]]

        if target_value == self._key_values[-1]:
            self._current_index = len(self._key_values) - 1
            return self._index[self._key_values[-1]]

        # Determine search bounds
        last_index_value = self._current_index if self._current_index is not None else 0
        if target_value < self._key_values[last_index_value]:
            last_index_value = 0  # Reset if target is lower than last found

        # Try linear vicinity search first
        result = self._linear_vicinity_search(target_value)
        if result is not None:
            return result

        # Fallback to binary search
        lower_index, upper_index = last_index_value, len(self._key_values) - 1
        # Binary search with proximity tracking
        best_key = self._key_values[lower_index]
        min_diff = abs(best_key - target_value)

        while lower_index <= upper_index:
            mid = (lower_index + upper_index) // 2
            mid_index = self._key_values[mid]
            diff = abs(mid_index - target_value)

            if diff < min_diff:
                min_diff = diff
                best_key = mid_index

            if mid_index < target_value:
                lower_index = mid + 1
            elif mid_index > target_value:
                upper_index = mid - 1
            else:
                self._current_index = mid
                return self._index[mid_index]  # Exact match

        self._current_index = self._key_values.index(best_key)
        return self._index[best_key]

    def get_data_by_key(self, key: Any) -> Dict | None:
        """return the value and the dict key from the data"""
        try:
            return self._data[key]
        except (IndexError, ValueError, KeyError):
            # print(f"{C_E} Value [{key}] is is not an index value{C_0}")
            return None

    def get_data_by_value(self, value: float | int) -> Dict:
        """does a search and returns a result dict containing search value, key and data"""
        _value = value
        _key = None
        _data = None

        try:
            _key = self.search(_value)
            _data = self.get_data_by_key(_key)
            _return = _data.get(self._sort_key)
            return {"input": _value, "return": _return, "key": _key, "data": _data, "field": self._sort_key}
        except (IndexError, ValueError, AttributeError):
            print(
                f"{C_W}🚨 Binary Sorter: Value [{_value}] couldn't be found in data in field [{self._sort_key}] or in Index {C_0}"
            )
            return None


def run_test(sample_data, sequence, label, linear_range):
    """Testing the binary search performance for different use cases"""
    sorter = BinarySorter(sample_data, sort_key="score")
    start = time.time()
    for val in sequence:
        _ = sorter.search(val)
    end = time.time()
    s = f"⏱️ {label} runtime: {end - start:.6f} seconds"
    return s


def test_get_data1():
    sample = {
        "alpha": {"score": 10},
        "beta": {"score": 20},
        "gamma": {"score": 30},
    }

    sorter = BinarySorter(sample, sort_key="score")
    value = 21.0
    key = sorter.search(value)
    print(f"value {value} got key {key} ")
    data = sorter.get_data_by_key(key)
    print(f"data1 {data}")
    data2 = sorter.get_data_by_value(14.0)
    print(f"data1 {data2}")


def test_get_data2():
    sample = [
        {"score": 10},
        {"score": 20},
        {"score": 30},
    ]

    sorter = BinarySorter(sample, sort_key="score")

    data2 = sorter.get_data_by_value(30.0)
    print(f"data2 {data2}")


if __name__ == "__main__":
    # test dict
    test_get_data1()
    # test list
    test_get_data2()
    if False:
        sample_data = {f"id_{i}": {"score": i * 0.1} for i in range(10000)}
        seq1 = [i * 0.1 for i in range(10000)]
        seq2 = [i * 0.1 if i % 2 == 0 else 99.9 - i * 0.1 for i in range(10000)]
        s1 = run_test(sample_data, seq1, "Sequential (optimized)", 0)
        s2 = run_test(sample_data, seq2, "Alternating (reset-heavy)", 0)
        s3 = run_test(sample_data, seq1, "Sequential (optimized) linear", 50)
        s4 = run_test(sample_data, seq2, "Alternating (reset-heavy) lineat", 50)

        # show runtimes for getting indices if entries are sorted vs unsorted
        print(s1)
        print(s2)
        print(s3)
        print(s4)
