from airtableformulahelpers import AND, NOT, OR, BooleanField


def test_bool_field_equals_true():
    """Test BoolField equals with True"""
    field = BooleanField(name="IsActive")
    result = field.equals(True)
    assert result == "{IsActive}=TRUE()"


def test_bool_field_equals_false():
    """Test BoolField equals with False"""
    field = BooleanField(name="IsActive")
    result = field.equals(False)
    assert result == "{IsActive}=FALSE()"


def test_bool_field_is_true():
    """Test BoolField is_true method"""
    field = BooleanField(name="Verified")
    result = field.is_true()
    assert result == "{Verified}=TRUE()"


def test_bool_field_is_false():
    """Test BoolField is_false method"""
    field = BooleanField(name="Verified")
    result = field.is_false()
    assert result == "{Verified}=FALSE()"


def test_bool_field_inheritance():
    """Test BoolField inherits from Field"""
    field = BooleanField(name="TestBool")

    # Test inherited methods
    assert field.is_empty() == "{TestBool}=BLANK()"
    assert field.is_not_empty() == "{TestBool}"
    assert field.name == "TestBool"


def test_bool_field_with_different_names():
    """Test BoolField with different field names"""
    fields = [
        BooleanField(name="Active"),
        BooleanField(name="Is Published"),
        BooleanField(name="has_permissions"),
        BooleanField(name="Flag-123"),
    ]

    for field in fields:
        assert field.is_true() == f"{{{field.name}}}=TRUE()"
        assert field.is_false() == f"{{{field.name}}}=FALSE()"


def test_bool_field_equals_method_behavior():
    """Test BoolField equals method with different boolean values"""
    field = BooleanField(name="Status")

    # Test with explicit boolean values
    assert field.equals(True) == "{Status}=TRUE()"
    assert field.equals(False) == "{Status}=FALSE()"


def test_bool_field_in_logical_operations():
    """Test BoolField in logical operations"""
    active_field = BooleanField(name="Active")
    verified_field = BooleanField(name="Verified")

    # Test with AND
    result = AND(active_field.is_true(), verified_field.is_true())
    assert result == "AND({Active}=TRUE(),{Verified}=TRUE())"

    # Test with OR
    result = OR(active_field.is_false(), verified_field.is_false())
    assert result == "OR({Active}=FALSE(),{Verified}=FALSE())"

    # Test with NOT
    result = NOT(active_field.is_true())
    assert result == "NOT({Active}=TRUE())"
