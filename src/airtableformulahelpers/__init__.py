from datetime import datetime
from typing import Literal, Optional, overload

import dateparser
from pydantic import BaseModel

COMPARISON = Literal["=", "!=", ">", "<", ">=", "<="]


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

    def THEN(self, value_if_true: str, string: bool = False) -> "ELSE":  # noqa: N802
        return ELSE(condition=self.condition, true_value=value_if_true, is_true_string=string)


class ELSE(THEN):
    true_value: str
    is_true_string: bool = False

    def ELSE(self, value_if_false: str, string: bool = False) -> str:  # noqa: N802
        true_val = f'"{self.true_value}"' if self.is_true_string else self.true_value
        false_val = f'"{value_if_false}"' if string else value_if_false
        return f"IF({self.condition}, {true_val}, {false_val})"


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

    def _find(
        self, value: str, comparison: str, case_sensitive: bool = False, no_trim: bool = False
    ) -> str:
        """case-insensitive"""
        if case_sensitive:
            if no_trim:
                return f'FIND("{value}", {{{self.name}}}){comparison}'
            else:
                return f'FIND(TRIM("{value}"), TRIM({{{self.name}}})){comparison}'
        else:
            if no_trim:
                return f'FIND(LOWER("{value}"), LOWER({{{self.name}}})){comparison}'
            else:
                return f'FIND(TRIM(LOWER("{value}")), TRIM(LOWER({{{self.name}}}))){comparison}'

    def contains(self, value: str, case_sensitive: bool = False, no_trim: bool = False) -> str:
        """case-insensitive"""
        return self._find(value, ">0", case_sensitive=case_sensitive, no_trim=no_trim)

    def not_contains(self, value: str, case_sensitive: bool = False, no_trim: bool = False) -> str:
        """case-insensitive"""
        return self._find(value, "=0", case_sensitive=case_sensitive, no_trim=no_trim)

    def starts_with(self, value: str, case_sensitive: bool = False, no_trim: bool = False) -> str:
        """case-insensitive"""
        return self._find(value, "=1", case_sensitive=case_sensitive, no_trim=no_trim)

    def not_starts_with(
        self, value: str, case_sensitive: bool = False, no_trim: bool = False
    ) -> str:
        """case-insensitive"""
        return self._find(value, "!=1", case_sensitive=case_sensitive, no_trim=no_trim)

    def _ends_with(
        self, value: str, comparison: str, case_sensitive: bool = False, no_trim: bool = False
    ) -> str:
        """case-insensitive"""
        if case_sensitive:
            if no_trim:
                return f'FIND("{value}", {{{self.name}}}) {comparison} LEN({{{self.name}}}) - LEN("{value}") + 1'
            else:
                return f'FIND(TRIM("{value}"), TRIM({{{self.name}}})) {comparison} LEN(TRIM({{{self.name}}})) - LEN(TRIM("{value}")) + 1'
        else:
            if no_trim:
                return f'FIND(LOWER("{value}"), LOWER({{{self.name}}})) {comparison} LEN(LOWER({{{self.name}}})) - LEN(LOWER("{value}")) + 1'
            else:
                return f'FIND(TRIM(LOWER("{value}")), TRIM(LOWER({{{self.name}}}))) {comparison} LEN(TRIM(LOWER({{{self.name}}}))) - LEN(TRIM(LOWER("{value}"))) + 1'

    def ends_with(self, value: str, case_sensitive: bool = False, no_trim: bool = False) -> str:
        """case-insensitive"""
        return self._ends_with(value, "=", case_sensitive=case_sensitive, no_trim=no_trim)

    def not_ends_with(self, value: str, case_sensitive: bool = False, no_trim: bool = False) -> str:
        """case-insensitive"""
        return self._ends_with(value, "!=", case_sensitive=case_sensitive, no_trim=no_trim)

    def regex_match(self, pattern: str) -> str:
        return f'REGEX_MATCH({{{self.name}}}, "{pattern}")'


class TextListField(Field):
    """String list comparison formulas"""

    def contains(self, value: str, case_sensitive: bool = False) -> str:
        if case_sensitive:
            return f'FIND("{value}", {{{self.name}}})>0'
        else:
            return f'FIND(LOWER("{value}"), LOWER({{{self.name}}}))>0'

    def not_contains(self, value: str, case_sensitive: bool = False) -> str:
        if case_sensitive:
            return f'FIND("{value}", {{{self.name}}})=0'
        else:
            return f'FIND(LOWER("{value}"), LOWER({{{self.name}}}))=0'

    def contains_all(self, values: list[str], case_sensitive: bool = False) -> str:
        return AND(*[self.contains(value, case_sensitive=case_sensitive) for value in values])

    def contains_any(self, values: list[str], case_sensitive: bool = False) -> str:
        return OR(*[self.contains(value, case_sensitive=case_sensitive) for value in values])


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
