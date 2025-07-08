from airtableformulahelpers import TextField


def test_text_field_equals():
    """Test TextField equals method"""
    field = TextField(name="Name")
    result = field.equals("John")
    assert result == '{Name}="John"'


def test_text_field_not_equals():
    """Test TextField not_equals method"""
    field = TextField(name="Name")
    result = field.not_equals("John")
    assert result == '{Name}!="John"'


def test_text_field_contains():
    """Test TextField contains method (case-insensitive)"""
    field = TextField(name="Description")
    result = field.contains("test")
    assert result == 'FIND(TRIM(LOWER("test")), TRIM(LOWER({Description})))>0'


def test_text_field_not_contains():
    """Test TextField not_contains method (case-insensitive)"""
    field = TextField(name="Description")
    result = field.not_contains("test")
    assert result == 'FIND(TRIM(LOWER("test")), TRIM(LOWER({Description})))=0'


def test_text_field_starts_with():
    """Test TextField starts_with method (case-insensitive)"""
    field = TextField(name="Title")
    result = field.starts_with("Mr")
    assert result == 'FIND(TRIM(LOWER("Mr")), TRIM(LOWER({Title})))=1'


def test_text_field_not_starts_with():
    """Test TextField not_starts_with method (case-insensitive)"""
    field = TextField(name="Title")
    result = field.not_starts_with("Mr")
    assert result == 'FIND(TRIM(LOWER("Mr")), TRIM(LOWER({Title})))!=1'


def test_text_field_ends_with():
    """Test TextField ends_with method (case-insensitive)"""
    field = TextField(name="Email")
    result = field.ends_with(".com")
    expected = 'FIND(TRIM(LOWER(".com")), TRIM(LOWER({Email}))) = LEN(TRIM(LOWER({Email}))) - LEN(TRIM(LOWER(".com"))) + 1'
    assert result == expected


def test_text_field_not_ends_with():
    """Test TextField not_ends_with method (case-insensitive)"""
    field = TextField(name="Email")
    result = field.not_ends_with(".com")
    expected = 'FIND(TRIM(LOWER(".com")), TRIM(LOWER({Email}))) != LEN(TRIM(LOWER({Email}))) - LEN(TRIM(LOWER(".com"))) + 1'
    assert result == expected


def test_text_field_regex_match():
    """Test TextField regex_match method"""
    field = TextField(name="Phone")
    result = field.regex_match(r"^\d{3}-\d{3}-\d{4}$")
    assert result == r'REGEX_MATCH({Phone}, "^\d{3}-\d{3}-\d{4}$")'


def test_text_field_with_special_characters():
    """Test TextField with special characters in values"""
    field = TextField(name="Data")

    # Test with quotes
    result = field.equals('Text with "quotes"')
    assert result == '{Data}="Text with "quotes""'

    # Test with apostrophes
    result = field.equals("Text with 'apostrophes'")
    assert result == "{Data}=\"Text with 'apostrophes'\""


def test_text_field_with_empty_values():
    """Test TextField with empty values"""
    field = TextField(name="Optional")
    result = field.equals("")
    assert result == '{Optional}=""'


def test_text_field_inheritance():
    """Test TextField inherits from Field"""
    field = TextField(name="TestField")

    # Test inherited methods
    assert field.is_empty() == "{TestField}=BLANK()"
    assert field.is_not_empty() == "{TestField}"
    assert field.name == "TestField"


def test_text_field_complex_regex():
    """Test TextField with complex regex patterns"""
    field = TextField(name="Code")

    # Email pattern
    result = field.regex_match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    assert result == r'REGEX_MATCH({Code}, "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")'


def test_text_field_find_method_edge_cases():
    """Test TextField _find method with edge cases"""
    field = TextField(name="Content")

    # Test with numbers
    result = field.contains("123")
    assert result == 'FIND(TRIM(LOWER("123")), TRIM(LOWER({Content})))>0'

    # Test with special characters
    result = field.contains("@#$")
    assert result == 'FIND(TRIM(LOWER("@#$")), TRIM(LOWER({Content})))>0'


def test_text_field_with_very_long_strings():
    """Test TextField with very long strings"""
    field = TextField(name="LongText")
    long_string = "A" * 1000  # 1000 character string

    result = field.equals(long_string)
    assert result == f'{{LongText}}="{long_string}"'


def test_unicode_and_special_characters_in_values():
    """Test fields with unicode and special characters in values"""
    field = TextField(name="Unicode")

    # Test with emoji
    assert field.equals("Hello 👋") == '{Unicode}="Hello 👋"'

    # Test with unicode characters
    assert field.equals("Café") == '{Unicode}="Café"'

    # Test with special symbols
    assert field.equals("Price: $50.00") == '{Unicode}="Price: $50.00"'


def test_regex_with_complex_patterns():
    """Test TextField regex with complex patterns"""
    field = TextField(name="Pattern")

    # Complex email regex
    email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    result = field.regex_match(email_pattern)
    assert result == f'REGEX_MATCH({{Pattern}}, "{email_pattern}")'
