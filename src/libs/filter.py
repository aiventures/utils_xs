"""filter.py Filtering Features"""

from abc import ABC, abstractmethod
from model.model_filter import (
    StrFilterModel,
    IncludeType,
    FilterTextOperation,
    LogicalOperator,
    BaseFilterModel,
    FilterModel,
    FilterType,
    BoolOpType,
)
from typing import Optional, Any
import logging
import re
from re import Pattern
from config.color_logger import setup_color_logging

# ensure root logger will use colored logger
setup_color_logging(use_color=True, use_emoji=True, indent=120)
logger = logging.getLogger(__name__)


class Filter(ABC):
    """Abstract Filter Class"""

    def __init__(self, filter: FilterModel):
        self._filter: FilterModel = filter

    @property
    def type(self) -> FilterType:
        """returns the filter type"""
        return self._filter.type

    @property
    def key(self) -> Optional[str]:
        """returns the filter type"""
        return self._filter.key

    @property
    def description(self) -> Optional[str]:
        """returns the filter type"""
        return self._filter.description

    @property
    def groups(self) -> list[str]:
        """returns the filter type"""
        return self._filter.groups

    @property
    def bool_op(self) -> Optional[BoolOpType]:
        """returns the filter type"""
        return self._filter.bool_op

    @property
    def include(self) -> Optional[IncludeType]:
        """returns the filter type"""
        return self._filter.include

    @property
    def ignore_none(self) -> bool:
        """returns the filter type"""
        return self._filter.ignore_none

    @abstractmethod
    def match(self, value: Optional[Any]) -> bool:
        """Matching Method"""
        return False


class StrFilter(Filter):
    """Atomic Simple String Filter"""

    def __init__(
        self,
        # filter string and operation
        filter_value: Optional[str] = None,
        filter_action: FilterTextOperation = "contains",
        key: Optional[str] = None,
        description: Optional[str] = None,
        groups: list[str] = [],
        bool_op: BoolOpType = "OR",
        include: IncludeType = "include",
        # if set to True any None values to be tested will be ignored and filter is passed
        ignore_none: bool = False,
        # operator: LogicalOperator = "any",
        operation: FilterTextOperation = "contains",
        ignorecase: bool = True,
    ):
        """Constructor."""
        self._filter = StrFilterModel(
            key=key,
            description=description,
            groups=groups,
            bool_op=bool_op,
            include=include,
            ignore_none=ignore_none,
            operation=operation,
            action=filter_action,
            value=filter_value,
            ignorecase=ignorecase,
        )

        self._regex_flag = re.IGNORECASE if ignorecase else re.NOFLAG

    def match(self, value: Optional[Any]) -> bool:
        """Applies the filter and checks for passing filter"""
        _passed: bool = False
        # test against none values
        if value is None or self._filter.value is None:
            return True if self._filter.ignore_none else False

        _value: str = str(value).lower() if self._filter.ignorecase else str(value)
        _filter: str = self._filter.value.lower() if self._filter.ignorecase else self._filter.value

        # do the filtering
        if self._filter.action == "regex":
            _regex: Pattern = re.compile(self._filter.value, self._regex_flag)
            _passed = True if len(_regex.findall(_value)) > 0 else False
        elif self._filter.action == "contains":
            _passed = True if _filter in _value else False
        elif self._filter.action == "exact":
            _passed = True if _value == _filter else False
        else:
            logger.error(f"Filter has invalid operation [{self._filter.operation}]")

        if self._filter.include == "exclude":
            _passed = not _passed

        return _passed

    def __repr__(self):
        return self._filter.model_dump_json()


class FilterList(Filter):
    """Use a group a list of filters to do the filtering on a single value"""

    def __init__(self, filters: list[Filter]):
        self._filters: list[Filter] = filters

    def match(self, value):
        for _filter in self._filters:
            _filter.match(value)

        return super().match(value)

    # TODO add match by group


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    value: str = "dies ist ein test"
    str_filter = StrFilter(filter_value="dies ist ein test", filter_action="exact", bool_op="OR")
    # show the filter values
    print(repr(str_filter))
    print(
        f"HUGO [{str_filter.type}] must match {str_filter.match('dies ist ein test')} doesnt match {str_filter.match('hugo')}"
    )
