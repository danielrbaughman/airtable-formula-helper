from datetime import datetime
from typing import Literal, Optional, overload

import dateparser
from pydantic import BaseModel

COMPARISON = Literal["=", "!=", ">", "<", ">=", "<="]

# class Formula():
#     table: str
#     # use_field_ids: bool
#     # field_id_map: dict[str, str]

#     def __init__(self, table: str):
#         self.table = table


def AND(*args: str) -> str:  # noqa: N802
    return f"AND({','.join(args)})"


def OR(*args: str) -> str:  # noqa: N802
    return f"OR({','.join(args)})"


def XOR(*args: str) -> str:  # noqa: N802
    return f"XOR({','.join(args)})"


def NOT(*args: str) -> str:  # noqa: N802
    return f"NOT({','.join(args)})"


def IF(condition: str) -> "THEN":  # noqa: N802
    """Start an IF statement."""
    return THEN(condition=condition)


class THEN(BaseModel):
    condition: str

    def THEN(self, value_if_true: str) -> "ELSE":  # noqa: N802
        return ELSE(condition=self.condition, true_value=value_if_true)


class ELSE(THEN):
    true_value: str

    def ELSE(self, value_if_false: str) -> str:  # noqa: N802
        return f"IF({self.condition}, {self.true_value}, {value_if_false})"


def id_equals(id: str) -> str:
    return f"RECORD_ID()='{id}'"


class Field(BaseModel):
    name: str

    def is_empty(self) -> str:
        return f"{{{self.name}}}=BLANK()"
    
    def is_not_empty(self) -> str:
        return f"{{{self.name}}}"


class TextField(Field):
    """String comparison formulas"""

    def equals(self, value: str) -> str:
        return f'{{{self.name}}}="{value}"'

    def not_equals(self, value: str) -> str:
        return f'{{{self.name}}}!="{value}"'

    def _find(self, value: str, comparison: str) -> str:
        """case-insensitive"""
        return f'FIND(TRIM(LOWER("{value}")), TRIM(LOWER({{{self.name}}}))){comparison}'

    def contains(self, value: str) -> str:
        """case-insensitive"""
        return self._find(value, ">0")

    def not_contains(self, value: str) -> str:
        """case-insensitive"""
        return self._find(value, "=0")

    def starts_with(self, value: str) -> str:
        """case-insensitive"""
        return self._find(value, "=1")

    def not_starts_with(self, value: str) -> str:
        """case-insensitive"""
        return self._find(value, "!=1")

    def _ends_with(self, value: str, comparison: str) -> str:
        """case-insensitive"""
        return f'FIND(TRIM(LOWER("{value}")), TRIM(LOWER({{{self.name}}}))) {comparison} LEN(TRIM(LOWER({{{self.name}}}))) - LEN(TRIM(LOWER("{value}"))) + 1'

    def ends_with(self, value: str) -> str:
        """case-insensitive"""
        return self._ends_with(value, "=")

    def not_ends_with(self, value: str) -> str:
        """case-insensitive"""
        return self._ends_with(value, "!=")

    def regex_match(self, pattern: str) -> str:
        return f'REGEX_MATCH({{{self.name}}}, "{pattern}")'


class TextListField(Field):
    """String list comparison formulas"""

    def contains(self, value: str) -> str:
        return f'FIND(LOWER("{value}"), LOWER({{{self.name}}}))>0'

    def not_contains(self, value: str) -> str:
        return f'FIND(LOWER("{value}"), LOWER({{{self.name}}}))=0'

    def contains_all(self, values: list[str]) -> str:
        return AND(*[self.contains(value) for value in values])

    def contains_any(self, values: list[str]) -> str:
        return OR(*[self.contains(value) for value in values])


class NumberField(Field):
    """Number comparison formulas"""

    def _compare(self, comparison: COMPARISON, value: int | float) -> str:
        return f"{{{self.name}}}{comparison}{value}"

    def equals(self, value: int | float) -> str:
        return self._compare("=", value)

    def not_equals(self, value: int | float) -> str:
        return self._compare("!=", value)

    def greater_than(self, value: int | float) -> str:
        return self._compare(">", value)

    def less_than(self, value: int | float) -> str:
        return self._compare("<", value)

    def greater_than_or_equals(self, value: int | float) -> str:
        return self._compare(">=", value)

    def less_than_or_equals(self, value: int | float) -> str:
        return self._compare("<=", value)


class BooleanField(Field):
    """Boolean comparison formulas"""

    def equals(self, value: bool) -> str:
        return f"{{{self.name}}}={'TRUE()' if value else 'FALSE()'}"

    def is_true(self) -> str:
        return f"{{{self.name}}}=TRUE()"

    def is_false(self) -> str:
        return f"{{{self.name}}}=FALSE()"


class AttachmentsField(Field):
    """Attachment comparison formulas"""

    def is_not_empty(self) -> str:
        return f"LEN({{{self.name}}})>0"

    def is_empty(self) -> str:
        return f"LEN({{{self.name}}})=0"

    def count_is(self, count: int) -> str:
        return f"LEN({{{self.name}}})={count}"

def _parse_date(date: datetime | str) -> datetime:
    if isinstance(date, datetime):
        parsed_date = date
    else:
        result: datetime | None = dateparser.parse(date)
        if result is None:
            raise ValueError(f"Could not parse date: {date}")
        parsed_date: datetime = result
    return parsed_date

class DateComparison(Field):
    compare: COMPARISON

    def _date(self, date: str | datetime) -> str:
        parsed_date = _parse_date(date)
        return f"DATETIME_PARSE('{parsed_date}'){self.compare}DATETIME_PARSE({{{self.name}}})"

    def _ago(self, unit: str, value: int) -> str:
        return f"DATETIME_DIFF(NOW(), {{{self.name}}}, '{unit}'){self.compare}{value}"

    def milliseconds_ago(self, milliseconds: int) -> str:
        return self._ago("milliseconds", milliseconds)

    def seconds_ago(self, seconds: int) -> str:
        return self._ago("seconds", seconds)

    def minutes_ago(self, minutes: int) -> str:
        return self._ago("minutes", minutes)

    def hours_ago(self, hours: int) -> str:
        return self._ago("hours", hours)

    def days_ago(self, days: int) -> str:
        return self._ago("days", days)

    def weeks_ago(self, weeks: int) -> str:
        return self._ago("weeks", weeks)

    def months_ago(self, months: int) -> str:
        return self._ago("months", months)

    def quarters_ago(self, quarters: int) -> str:
        return self._ago("quarters", quarters)

    def years_ago(self, years: int) -> str:
        return self._ago("years", years)

class DateField(Field):
    """DateTime comparison formulas"""

    @overload
    def is_on(self) -> DateComparison: ...
    @overload
    def is_on(self, date: str | datetime) -> str: ...
    def is_on(self, date: Optional[str | datetime] = None) -> DateComparison | str:
        date_comparison = DateComparison(name=self.name, compare="=")
        if date is None:
            return date_comparison

        parsed_date: datetime = _parse_date(date)
        return date_comparison._date(parsed_date)

    @overload
    def is_on_or_after(self) -> DateComparison: ...
    @overload
    def is_on_or_after(self, date: str | datetime) -> str: ...
    def is_on_or_after(self, date: Optional[str | datetime] = None) -> DateComparison | str:
        date_comparison = DateComparison(name=self.name, compare=">=")
        if date is None:
            return date_comparison

        parsed_date: datetime = _parse_date(date)
        return date_comparison._date(parsed_date)

    @overload
    def is_on_or_before(self) -> DateComparison: ...
    @overload
    def is_on_or_before(self, date: str | datetime) -> str: ...
    def is_on_or_before(self, date: Optional[str | datetime] = None) -> DateComparison | str:
        date_comparison = DateComparison(name=self.name, compare="<=")
        if date is None:
            return date_comparison

        parsed_date: datetime = _parse_date(date)
        return date_comparison._date(parsed_date)

    @overload
    def is_after(self) -> DateComparison: ...
    @overload
    def is_after(self, date: str | datetime) -> str: ...
    def is_after(self, date: Optional[str | datetime] = None) -> DateComparison | str:
        date_comparison = DateComparison(name=self.name, compare="<")
        if date is None:
            return date_comparison

        parsed_date: datetime = _parse_date(date)
        return date_comparison._date(parsed_date)

    @overload
    def is_before(self) -> DateComparison: ...
    @overload
    def is_before(self, date: str | datetime) -> str: ...
    def is_before(self, date: Optional[str | datetime] = None) -> DateComparison | str:
        date_comparison = DateComparison(name=self.name, compare=">")
        if date is None:
            return date_comparison

        parsed_date: datetime = _parse_date(date)
        return date_comparison._date(parsed_date)

    @overload
    def is_not_on(self) -> DateComparison: ...
    @overload
    def is_not_on(self, date: str | datetime) -> str: ...
    def is_not_on(self, date: Optional[str | datetime] = None) -> DateComparison | str:
        date_comparison = DateComparison(name=self.name, compare="!=")
        if date is None:
            return date_comparison

        parsed_date: datetime = _parse_date(date)
        return date_comparison._date(parsed_date)
