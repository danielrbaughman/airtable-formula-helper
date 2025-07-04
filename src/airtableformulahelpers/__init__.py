from typing import Literal

import dateparser
from pydantic import BaseModel

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


def IF(condition: str, true_value: str, false_value: str) -> str:  # noqa: N802
    return f"IF({condition}, {true_value}, {false_value})"




def id_equals(id: str) -> str:
    return f"RECORD_ID()='{id}'"

class Field(BaseModel):
    name: str

    def is_empty(self) -> str:
        return f"{{{self.name}}}=BLANK()"

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
    """List comparison formulas"""

    def contains(self, value: str) -> str:
        return f'FIND(LOWER("{value}"), LOWER({{{self.name}}}))>0'

    def not_contains(self, value: str) -> str:
        return f'FIND(LOWER("{value}"), LOWER({{{self.name}}}))=0'

    def contains_all(self, values: list[str]) -> str:
        return AND(*[self.contains(value) for value in values])

    def contains_any(self, values: list[str]) -> str:
        return OR(*[self.contains(value) for value in values])

COMPARISON = Literal["=", "!=", ">", "<", ">=", "<="]

class Number(Field):
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


class DateComparison(Field):
    compare: COMPARISON

    def value(self, date: str) -> str:
        parsed_date = dateparser.parse(date)
        return f"DATETIME_PARSE('{parsed_date}'){self.compare}DATETIME_PARSE({{{self.name}}})"

    def _ago(self, unit: str, value: int) -> str:
        return f"DATETIME_DIFF(NOW(), {{{self.name}}}, '{unit}'){self.compare}{value}"

    def milliseconds_ago(self, value: int) -> str:
        return self._ago("milliseconds", value)

    def seconds_ago(self, value: int) -> str:
        return self._ago("seconds", value)

    def minutes_ago(self, value: int) -> str:
        return self._ago("minutes", value)

    def hours_ago(self, value: int) -> str:
        return self._ago("hours", value)

    def days_ago(self, value: int) -> str:
        return self._ago("days", value)

    def weeks_ago(self, value: int) -> str:
        return self._ago("weeks", value)

    def months_ago(self, value: int) -> str:
        return self._ago("months", value)

    def quarters_ago(self, value: int) -> str:
        return self._ago("quarters", value)

    def years_ago(self, value: int) -> str:
        return self._ago("years", value)

class DateField(Field):
    """DateTime comparison formulas"""

    def is_on(self) -> DateComparison:
        return DateComparison(name=self.name, compare="=")
    
    def is_on_or_after(self) -> DateComparison:
        return DateComparison(name=self.name, compare=">=")

    def is_on_or_before(self) -> DateComparison:
        return DateComparison(name=self.name, compare="<=")

    def is_after(self) -> DateComparison:
        return DateComparison(name=self.name, compare="<")
    
    def is_before(self) -> DateComparison:
        return DateComparison(name=self.name, compare=">")

    def is_not_on(self) -> DateComparison:
        return DateComparison(name=self.name, compare="!=")
