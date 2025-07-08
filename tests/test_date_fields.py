from datetime import datetime

import pytest

from airtableformulahelpers import DateComparison, DateField


def test_date_field_methods_with_invalid_date():
    """Test DateField methods with invalid date strings"""
    field = DateField(name="TestDate")

    with pytest.raises(ValueError):
        field.is_on("invalid-date")

    with pytest.raises(ValueError):
        field.is_before("not-a-date")

    with pytest.raises(ValueError):
        field.is_after("bad-date")

    with pytest.raises(ValueError):
        field.is_on_or_before("wrong-format")

    with pytest.raises(ValueError):
        field.is_on_or_after("invalid")

    with pytest.raises(ValueError):
        field.is_not_on("unparseable")


def test_date_comparison_date_method_with_invalid_date():
    """Test DateComparison _date method with invalid date strings"""
    comparison = DateComparison(name="TestDate", compare="=")

    with pytest.raises(ValueError):
        comparison._date("invalid-date")

    with pytest.raises(ValueError):
        comparison._date("not-a-date")


def test_date_field_is_on_with_datetime():
    """Test DateField is_on with datetime object"""
    field = DateField(name="Created")
    test_date = datetime(2023, 6, 15, 14, 30, 0)

    result = field.is_on(test_date)
    assert result == "DATETIME_PARSE('2023-06-15 14:30:00')=DATETIME_PARSE({Created})"


def test_date_field_is_on_with_string():
    """Test DateField is_on with string date"""
    field = DateField(name="Modified")

    result = field.is_on("2023-06-15")
    assert "DATETIME_PARSE(" in result
    assert "=DATETIME_PARSE({Modified})" in result


def test_date_field_is_on_returns_comparison():
    """Test DateField is_on returns DateComparison when no date provided"""
    field = DateField(name="TestDate")
    result = field.is_on()

    assert isinstance(result, DateComparison)
    assert result.name == "TestDate"
    assert result.compare == "="


def test_date_field_is_before_with_datetime():
    """Test DateField is_before with datetime object"""
    field = DateField(name="Deadline")
    test_date = datetime(2023, 12, 31, 23, 59, 59)

    result = field.is_before(test_date)
    assert result == "DATETIME_PARSE('2023-12-31 23:59:59')>DATETIME_PARSE({Deadline})"


def test_date_field_is_before_returns_comparison():
    """Test DateField is_before returns DateComparison when no date provided"""
    field = DateField(name="TestDate")
    result = field.is_before()

    assert isinstance(result, DateComparison)
    assert result.name == "TestDate"
    assert result.compare == ">"


def test_date_field_is_after_with_string():
    """Test DateField is_after with string date"""
    field = DateField(name="StartDate")

    result = field.is_after("2023-01-01")
    assert "DATETIME_PARSE(" in result
    assert "<DATETIME_PARSE({StartDate})" in result


def test_date_field_is_after_returns_comparison():
    """Test DateField is_after returns DateComparison when no date provided"""
    field = DateField(name="TestDate")
    result = field.is_after()

    assert isinstance(result, DateComparison)
    assert result.name == "TestDate"
    assert result.compare == "<"


def test_date_field_is_on_or_before_with_datetime():
    """Test DateField is_on_or_before with datetime object"""
    field = DateField(name="EventDate")
    test_date = datetime(2023, 7, 4, 12, 0, 0)

    result = field.is_on_or_before(test_date)
    assert result == "DATETIME_PARSE('2023-07-04 12:00:00')<=DATETIME_PARSE({EventDate})"


def test_date_field_is_on_or_before_returns_comparison():
    """Test DateField is_on_or_before returns DateComparison when no date provided"""
    field = DateField(name="TestDate")
    result = field.is_on_or_before()

    assert isinstance(result, DateComparison)
    assert result.name == "TestDate"
    assert result.compare == "<="


def test_date_field_is_on_or_after_with_string():
    """Test DateField is_on_or_after with string date"""
    field = DateField(name="LaunchDate")

    result = field.is_on_or_after("2023-03-15")
    assert "DATETIME_PARSE(" in result
    assert ">=DATETIME_PARSE({LaunchDate})" in result


def test_date_field_is_on_or_after_returns_comparison():
    """Test DateField is_on_or_after returns DateComparison when no date provided"""
    field = DateField(name="TestDate")
    result = field.is_on_or_after()

    assert isinstance(result, DateComparison)
    assert result.name == "TestDate"
    assert result.compare == ">="


def test_date_field_is_not_on_with_datetime():
    """Test DateField is_not_on with datetime object"""
    field = DateField(name="ExcludeDate")
    test_date = datetime(2023, 11, 25, 0, 0, 0)

    result = field.is_not_on(test_date)
    assert result == "DATETIME_PARSE('2023-11-25 00:00:00')!=DATETIME_PARSE({ExcludeDate})"


def test_date_field_is_not_on_returns_comparison():
    """Test DateField is_not_on returns DateComparison when no date provided"""
    field = DateField(name="TestDate")
    result = field.is_not_on()

    assert isinstance(result, DateComparison)
    assert result.name == "TestDate"
    assert result.compare == "!="


def test_date_field_inheritance():
    """Test DateField inherits from Field"""
    field = DateField(name="TestDate")

    # Test inherited methods
    assert field.is_empty() == "{TestDate}=BLANK()"
    assert field.is_not_empty() == "{TestDate}"
    assert field.name == "TestDate"


def test_date_field_with_edge_case_dates():
    """Test DateField with edge case dates like leap years"""
    field = DateField(name="LeapDate")

    # Test with leap year date
    result = field.is_on("2024-02-29")
    assert "DATETIME_PARSE(" in result
    assert "=DATETIME_PARSE({LeapDate})" in result


class TestDateComparison:
    """Tests for DateComparison class"""

    def test_date_comparison_milliseconds_ago(self):
        """Test DateComparison milliseconds_ago method"""
        comparison = DateComparison(name="LastSeen", compare=">=")
        result = comparison.milliseconds_ago(5000)
        assert result == "DATETIME_DIFF(NOW(), {LastSeen}, 'milliseconds')>=5000"

    def test_date_comparison_seconds_ago(self):
        """Test DateComparison seconds_ago method"""
        comparison = DateComparison(name="UpdatedAt", compare="<=")
        result = comparison.seconds_ago(30)
        assert result == "DATETIME_DIFF(NOW(), {UpdatedAt}, 'seconds')<=30"

    def test_date_comparison_minutes_ago(self):
        """Test DateComparison minutes_ago method"""
        comparison = DateComparison(name="LastActive", compare=">")
        result = comparison.minutes_ago(15)
        assert result == "DATETIME_DIFF(NOW(), {LastActive}, 'minutes')>15"

    def test_date_comparison_hours_ago(self):
        """Test DateComparison hours_ago method"""
        comparison = DateComparison(name="CreatedAt", compare="<")
        result = comparison.hours_ago(24)
        assert result == "DATETIME_DIFF(NOW(), {CreatedAt}, 'hours')<24"

    def test_date_comparison_days_ago(self):
        """Test DateComparison days_ago method"""
        comparison = DateComparison(name="PostDate", compare="=")
        result = comparison.days_ago(7)
        assert result == "DATETIME_DIFF(NOW(), {PostDate}, 'days')=7"

    def test_date_comparison_weeks_ago(self):
        """Test DateComparison weeks_ago method"""
        comparison = DateComparison(name="EventDate", compare="!=")
        result = comparison.weeks_ago(2)
        assert result == "DATETIME_DIFF(NOW(), {EventDate}, 'weeks')!=2"

    def test_date_comparison_months_ago(self):
        """Test DateComparison months_ago method"""
        comparison = DateComparison(name="BirthDate", compare=">=")
        result = comparison.months_ago(12)
        assert result == "DATETIME_DIFF(NOW(), {BirthDate}, 'months')>=12"

    def test_date_comparison_quarters_ago(self):
        """Test DateComparison quarters_ago method"""
        comparison = DateComparison(name="ReportDate", compare="<=")
        result = comparison.quarters_ago(4)
        assert result == "DATETIME_DIFF(NOW(), {ReportDate}, 'quarters')<=4"

    def test_date_comparison_years_ago(self):
        """Test DateComparison years_ago method"""
        comparison = DateComparison(name="StartDate", compare=">")
        result = comparison.years_ago(5)
        assert result == "DATETIME_DIFF(NOW(), {StartDate}, 'years')>5"

    def test_date_comparison_with_zero_values(self):
        """Test DateComparison with zero values"""
        comparison = DateComparison(name="Now", compare="=")

        assert comparison.seconds_ago(0) == "DATETIME_DIFF(NOW(), {Now}, 'seconds')=0"
        assert comparison.minutes_ago(0) == "DATETIME_DIFF(NOW(), {Now}, 'minutes')=0"
        assert comparison.hours_ago(0) == "DATETIME_DIFF(NOW(), {Now}, 'hours')=0"
        assert comparison.days_ago(0) == "DATETIME_DIFF(NOW(), {Now}, 'days')=0"
