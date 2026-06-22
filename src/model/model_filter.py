"""Generic Filter Model. partly copied from utils repo."""

from typing import List, Optional, Literal, Any, Annotated, Dict

# from datetime import datetime as DateTime
from pydantic import BaseModel, Field

# Constants
# type definitions

IncludeLiteral = Literal["include", "exclude"]
IncludeType = Annotated[IncludeLiteral, "Filter to Include/Exclude Search Result"]
FilterType = Annotated[Literal["text", "numerical"], "Type Of Filter"]
FilterTextOperation = Annotated[Literal["contains", "exact", "regex"], "Type Of Text Filter"]

# AnyOrAllType = Annotated[Literal["any", "all"], "Filter to Control whether ALL or ANY filters must match"]
# OperatorMin = Annotated[Literal["gt", "ge", "eq"], "Numerical Filter Lower Bound: greater than, greater equal, equal"]
# OperatorMax = Annotated[Literal["lt", "le", "eq"], "Numerical Filter Upper Bound: lower than, lower equal, equal"]


class BaseFilterModel(BaseModel):
    """Atomic Filter as Base Class for other filter types"""

    # key and description of filter
    key: Optional[str] = None
    description: Optional[str] = None
    filter_type: FilterType = "text"
    # group assignment
    groups: Optional[List[Any] | str] = None  # assignment to a filter group
    # include or exclude filter result (NOT logic)
    include: Optional[IncludeType] = "include"
    # if set any None values to be tested will be ignored and filter is passed
    ignore_none: bool = False


class StrFilterModel(BaseFilterModel):
    """Atomic String filter model"""

    type = "text"
    operation: FilterTextOperation = "contains"
    filter: Optional[str] = None
    ignorecase: bool = True


# class SimpleStrFilterModel(BaseModel):
#     """simple filtermodel for the Utils simple filter method"""

#     str_filter: list | str = None
#     any_or_all: Optional[AnyOrAllType] = "any"
#     match: Optional[StringMatch] = "contains"
#     include: Optional[IncludeType] = "include"
#     case_insensitive: Optional[bool] = True
#     sep: Optional[str] = ","


# class NumericalFilterModel(FilterModel):
#     """Filter for a numeric value"""

#     value_min: Optional[float | int | DateTime] = None
#     operator_min: Optional[OperatorMin] = "ge"

#     value_max: Optional[float | int | DateTime] = None
#     operator_max: Optional[OperatorMax] = "le"

#     # lower / lower equal operators

#     @field_validator("value_min", "value_max")
#     @classmethod
#     def validate(cls, value) -> float | int | DateTime:
#         """validation for numerical value"""
#         if value is not None and not isinstance(value, (int, float, DateTime)):
#             raise ValueError(f"[Filter] Got Value [{value}],expecting numerical type")
#         return value


# class RegexFilterModel(FilterModel):
#     """Filter for a regex string"""

#     regex: Optional[str] = None  # simply the regex string


# class StringFilterModel(FilterModel):
#     """Filtering a string"""

#     filter_strings: Optional[str | List[str]] = None  # string or list of strings to be matched
#     match: Optional[StringMatch] = "contains"  # str need to match excatly or only parts of it
#     string_operator: Optional[AnyOrAllType] = "any"  # same as oprator but on atomic filter level


# class ObjectFilterModel(FilterModel):
#     """Basically a Filter that can host Filters and Filter Sets by attribute"""

#     # Model is a list of [filter|filterset]
#     # using the attributes field, it is possible to do the filtering on attributes of
#     # a dict/list
#     # We can't specify the concrete object classes here as otherwise we'd risk
#     # circular imports
#     field_filters: Optional[List[object]] = []


# class FilterSetModel(FilterModel):
#     """representing the filter set moddel / Filter grouped into sets"""

#     filter_list: Optional[List[object]] = []


# class AtomicFilterResult(BaseModel):
#     """Return Structure of the filter result"""

#     filter_key: Optional[object] = None
#     obj: Optional[object] = None
#     operator: Optional[AnyOrAllType] = None
#     include: Optional[IncludeType] = None
#     attribute: Optional[str] = None
#     groups: Optional[list] = None
#     passed: Optional[bool] = None

# class FilterSetResult(BaseModel):
#     """Return Structure of the filter result"""

#     # results of each atomic filter
#     filters_result: Optional[List[AtomicFilterResult]] = []
#     # filter set result
#     filter_set_result: Optional[AtomicFilterResult] = None
#     # for the case error: dict of filter keys and error messages
#     messages: Optional[Dict[str, list]] = {}
#     # overall result
#     passed: Optional[bool] = None
