import dateparser


class DateComparison:
    compare: str

    def __init__(self, compare: str):
        self.compare = compare

    def value(self, field: str, date: str) -> str:
        parsed_date = dateparser.parse(date)
        return f"DATETIME_PARSE('{parsed_date}'){self.compare}DATETIME_PARSE({{{field}}})"

    def _ago(self, field: str, unit: str, value: int) -> str:
        return f"DATETIME_DIFF(NOW(), {{{field}}}, '{unit}'){self.compare}{value}"

    def milliseconds_ago(self, field: str, value: int) -> str:
        return self._ago(field, "milliseconds", value)

    def seconds_ago(self, field: str, value: int) -> str:
        return self._ago(field, "seconds", value)

    def minutes_ago(self, field: str, value: int) -> str:
        return self._ago(field, "minutes", value)

    def hours_ago(self, field: str, value: int) -> str:
        return self._ago(field, "hours", value)

    def days_ago(self, field: str, value: int) -> str:
        return self._ago(field, "days", value)

    def weeks_ago(self, field: str, value: int) -> str:
        return self._ago(field, "weeks", value)

    def months_ago(self, field: str, value: int) -> str:
        return self._ago(field, "months", value)

    def quarters_ago(self, field: str, value: int) -> str:
        return self._ago(field, "quarters", value)

    def years_ago(self, field: str, value: int) -> str:
        return self._ago(field, "years", value)


class ATFormula:
    """Abstracts Airtable formula syntax for easier use"""

    @staticmethod
    def id_equals(id: str) -> str:
        return f"RECORD_ID()='{id}'"

    @staticmethod
    def is_empty(field: str) -> str:
        return f"{{{field}}}=BLANK()"

    class Logic:
        """AND, OR, XOR, NOT, IF"""

        @staticmethod
        def AND(*args: str) -> str:  # noqa: N802
            return f"AND({','.join(args)})"

        @staticmethod
        def OR(*args: str) -> str:  # noqa: N802
            return f"OR({','.join(args)})"

        @staticmethod
        def XOR(*args: str) -> str:  # noqa: N802
            return f"XOR({','.join(args)})"

        @staticmethod
        def NOT(*args: str) -> str:  # noqa: N802
            return f"NOT({','.join(args)})"

        @staticmethod
        def IF(condition: str, true_value: str, false_value: str) -> str:  # noqa: N802
            """IF(condition, true_value, false_value)"""
            return f"IF({condition}, {true_value}, {false_value})"

    class String:
        """String comparison formulas"""

        @staticmethod
        def equals(field: str, value: str) -> str:
            return f'{{{field}}}="{value}"'

        @staticmethod
        def not_equals(field: str, value: str) -> str:
            return f'{{{field}}}!="{value}"'

        @staticmethod
        def _find(field: str, value: str, comparison: str) -> str:
            return f'FIND(TRIM(LOWER("{value}")), TRIM(LOWER({{{field}}}))){comparison}'

        @staticmethod
        def contains(field: str, value: str) -> str:
            return ATFormula.String._find(field, value, ">0")

        @staticmethod
        def not_contains(field: str, value: str) -> str:
            return ATFormula.String._find(field, value, "=0")

        @staticmethod
        def starts_with(field: str, value: str) -> str:
            return ATFormula.String._find(field, value, "=1")

        @staticmethod
        def not_starts_with(field: str, value: str) -> str:
            return ATFormula.String._find(field, value, "!=1")

        @staticmethod
        def _ends_with(field: str, value: str, comparison: str) -> str:
            return f'FIND(TRIM(LOWER("{value}")), TRIM(LOWER({{{field}}}))) {comparison} LEN(TRIM(LOWER({{{field}}}))) - LEN(TRIM(LOWER("{value}"))) + 1'

        @staticmethod
        def ends_with(field: str, value: str) -> str:
            return ATFormula.String._ends_with(field, value, "=")

        @staticmethod
        def not_ends_with(field: str, value: str) -> str:
            return ATFormula.String._ends_with(field, value, "!=")

        @staticmethod
        def regex_match(field: str, pattern: str) -> str:
            return f'REGEX_MATCH({{{field}}}, "{pattern}")'

    class StringList:
        """List comparison formulas"""

        @staticmethod
        def contains(field: str, value: str) -> str:
            return f'FIND(LOWER("{value}"), LOWER({{{field}}}))>0'

        @staticmethod
        def not_contains(field: str, value: str) -> str:
            return f'FIND(LOWER("{value}"), LOWER({{{field}}}))=0'

        @staticmethod
        def contains_all(field: str, values: list[str]) -> str:
            return ATFormula.Logic.AND(
                *[ATFormula.StringList.contains(field, value) for value in values]
            )

        @staticmethod
        def contains_any(field: str, values: list[str]) -> str:
            return ATFormula.Logic.OR(
                *[ATFormula.StringList.contains(field, value) for value in values]
            )

    class Number:
        """Number comparison formulas"""

        @staticmethod
        def _compare(field: str, comparison: str, value: int | float) -> str:
            return f"{{{field}}}{comparison}{value}"

        @staticmethod
        def equals(field: str, value: int | float) -> str:
            return ATFormula.Number._compare(field, "=", value)

        @staticmethod
        def not_equals(field: str, value: int | float) -> str:
            return ATFormula.Number._compare(field, "!=", value)

        @staticmethod
        def greater_than(field: str, value: int | float) -> str:
            return ATFormula.Number._compare(field, ">", value)

        @staticmethod
        def less_than(field: str, value: int | float) -> str:
            return ATFormula.Number._compare(field, "<", value)

        @staticmethod
        def greater_than_or_equals(field: str, value: int | float) -> str:
            return ATFormula.Number._compare(field, ">=", value)

        @staticmethod
        def less_than_or_equals(field: str, value: int | float) -> str:
            return ATFormula.Number._compare(field, "<=", value)

    class Boolean:
        """Boolean comparison formulas"""

        @staticmethod
        def equals(field: str, value: bool) -> str:
            return f"{{{field}}}={'TRUE()' if value else 'FALSE()'}"

        @staticmethod
        def is_true(field: str) -> str:
            return f"{{{field}}}=TRUE()"

        @staticmethod
        def is_false(field: str) -> str:
            return f"{{{field}}}=FALSE()"

    class Attachments:
        """Attachment comparison formulas"""

        @staticmethod
        def exist(column_name: str) -> str:
            return f"LEN({{{column_name}}})>0"

        @staticmethod
        def not_exist(column_name: str) -> str:
            return f"LEN({{{column_name}}})=0"

        @staticmethod
        def count_is(column_name: str, count: int) -> str:
            return f"LEN({{{column_name}}})={count}"

    class DateTime:
        """DateTime comparison formulas"""

        class Equals(DateComparison):
            def __init__(self):
                super().__init__("=")

        class OnOrAfter(DateComparison):
            def __init__(self):
                super().__init__("<=")

        class OnOrBefore(DateComparison):
            def __init__(self):
                super().__init__(">=")

        class After(DateComparison):
            def __init__(self):
                super().__init__("<")

        class Before(DateComparison):
            def __init__(self):
                super().__init__(">")

        class NotEquals(DateComparison):
            def __init__(self):
                super().__init__("!=")
