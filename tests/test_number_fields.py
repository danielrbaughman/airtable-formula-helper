from airtableformulahelpers import NumberField


def test_number_field_equals_int():
    """Test Number field equals with integer"""
    field = NumberField(name="Score")
    result = field.equals(100)
    assert result == "{Score}=100"


def test_number_field_equals_float():
    """Test Number field equals with float"""
    field = NumberField(name="Price")
    result = field.equals(99.99)
    assert result == "{Price}=99.99"


def test_number_field_not_equals_int():
    """Test Number field not_equals with integer"""
    field = NumberField(name="Score")
    result = field.not_equals(0)
    assert result == "{Score}!=0"


def test_number_field_not_equals_float():
    """Test Number field not_equals with float"""
    field = NumberField(name="Price")
    result = field.not_equals(0.0)
    assert result == "{Price}!=0.0"


def test_number_field_greater_than():
    """Test Number field greater_than method"""
    field = NumberField(name="Age")
    result = field.greater_than(18)
    assert result == "{Age}>18"


def test_number_field_less_than():
    """Test Number field less_than method"""
    field = NumberField(name="Age")
    result = field.less_than(65)
    assert result == "{Age}<65"


def test_number_field_greater_than_or_equals():
    """Test Number field greater_than_or_equals method"""
    field = NumberField(name="Grade")
    result = field.greater_than_or_equals(70)
    assert result == "{Grade}>=70"


def test_number_field_less_than_or_equals():
    """Test Number field less_than_or_equals method"""
    field = NumberField(name="Grade")
    result = field.less_than_or_equals(100)
    assert result == "{Grade}<=100"


def test_number_field_with_negative_numbers():
    """Test Number field with negative numbers"""
    field = NumberField(name="Temperature")

    assert field.equals(-10) == "{Temperature}=-10"
    assert field.greater_than(-5) == "{Temperature}>-5"
    assert field.less_than(-15) == "{Temperature}<-15"


def test_number_field_with_zero():
    """Test Number field with zero"""
    field = NumberField(name="Count")

    assert field.equals(0) == "{Count}=0"
    assert field.not_equals(0) == "{Count}!=0"
    assert field.greater_than(0) == "{Count}>0"
    assert field.less_than(0) == "{Count}<0"


def test_number_field_with_large_numbers():
    """Test Number field with large numbers"""
    field = NumberField(name="Population")

    assert field.equals(1000000) == "{Population}=1000000"
    assert field.greater_than(999999) == "{Population}>999999"


def test_number_field_with_decimal_precision():
    """Test Number field with decimal precision"""
    field = NumberField(name="Precision")

    assert field.equals(3.14159) == "{Precision}=3.14159"
    assert field.greater_than(0.001) == "{Precision}>0.001"


def test_number_field_inheritance():
    """Test Number field inherits from Field"""
    field = NumberField(name="TestNumber")

    # Test inherited methods
    assert field.is_empty() == "{TestNumber}=BLANK()"
    assert field.is_not_empty() == "{TestNumber}"
    assert field.name == "TestNumber"


def test_number_field_compare_method():
    """Test Number field _compare method indirectly"""
    field = NumberField(name="Value")

    # Test all comparison operators
    assert field._compare("=", 10) == "{Value}=10"
    assert field._compare("!=", 10) == "{Value}!=10"
    assert field._compare(">", 10) == "{Value}>10"
    assert field._compare("<", 10) == "{Value}<10"
    assert field._compare(">=", 10) == "{Value}>=10"
    assert field._compare("<=", 10) == "{Value}<=10"


def test_number_field_with_extreme_values():
    """Test Number field with extreme values"""
    field = NumberField(name="Extreme")

    # Test very large numbers
    assert field.equals(999999999999) == "{Extreme}=999999999999"

    # Test very small decimals
    assert field.equals(0.000001) == "{Extreme}=1e-06"

    # Test negative large numbers
    assert field.equals(-999999999999) == "{Extreme}=-999999999999"
