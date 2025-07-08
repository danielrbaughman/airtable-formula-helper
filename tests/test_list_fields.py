from airtableformulahelpers import TextListField


def test_list_field_contains():
    """Test ListField contains method (case-insensitive)"""
    field = TextListField(name="Tags")
    result = field.contains("urgent")
    assert result == 'FIND(LOWER("urgent"), LOWER({Tags}))>0'


def test_list_field_not_contains():
    """Test ListField not_contains method (case-insensitive)"""
    field = TextListField(name="Tags")
    result = field.not_contains("urgent")
    assert result == 'FIND(LOWER("urgent"), LOWER({Tags}))=0'


def test_list_field_contains_all():
    """Test ListField contains_all method"""
    field = TextListField(name="Skills")
    result = field.contains_all(["python", "javascript", "sql"])
    expected = 'AND(FIND(LOWER("python"), LOWER({Skills}))>0,FIND(LOWER("javascript"), LOWER({Skills}))>0,FIND(LOWER("sql"), LOWER({Skills}))>0)'
    assert result == expected


def test_list_field_contains_any():
    """Test ListField contains_any method"""
    field = TextListField(name="Skills")
    result = field.contains_any(["python", "javascript", "sql"])
    expected = 'OR(FIND(LOWER("python"), LOWER({Skills}))>0,FIND(LOWER("javascript"), LOWER({Skills}))>0,FIND(LOWER("sql"), LOWER({Skills}))>0)'
    assert result == expected


def test_list_field_contains_all_single_item():
    """Test ListField contains_all with single item"""
    field = TextListField(name="Categories")
    result = field.contains_all(["business"])
    expected = 'AND(FIND(LOWER("business"), LOWER({Categories}))>0)'
    assert result == expected


def test_list_field_contains_any_single_item():
    """Test ListField contains_any with single item"""
    field = TextListField(name="Categories")
    result = field.contains_any(["business"])
    expected = 'OR(FIND(LOWER("business"), LOWER({Categories}))>0)'
    assert result == expected


def test_list_field_contains_all_empty_list():
    """Test ListField contains_all with empty list"""
    field = TextListField(name="Empty")
    result = field.contains_all([])
    assert result == "AND()"


def test_list_field_contains_any_empty_list():
    """Test ListField contains_any with empty list"""
    field = TextListField(name="Empty")
    result = field.contains_any([])
    assert result == "OR()"


def test_list_field_with_special_characters():
    """Test ListField with special characters in values"""
    field = TextListField(name="Data")

    # Test with spaces
    result = field.contains("web development")
    assert result == 'FIND(LOWER("web development"), LOWER({Data}))>0'

    # Test with special characters
    result = field.contains("C++")
    assert result == 'FIND(LOWER("C++"), LOWER({Data}))>0'


def test_list_field_inheritance():
    """Test ListField inherits from Field"""
    field = TextListField(name="TestList")

    # Test inherited methods
    assert field.is_empty() == "{TestList}=BLANK()"
    assert field.is_not_empty() == "{TestList}"
    assert field.name == "TestList"


def test_list_field_case_insensitive():
    """Test ListField case insensitive behavior"""
    field = TextListField(name="Items")

    # Test with mixed case
    result = field.contains("Python")
    assert result == 'FIND(LOWER("Python"), LOWER({Items}))>0'

    result = field.contains_all(["JAVA", "python", "Go"])
    expected = 'AND(FIND(LOWER("JAVA"), LOWER({Items}))>0,FIND(LOWER("python"), LOWER({Items}))>0,FIND(LOWER("Go"), LOWER({Items}))>0)'
    assert result == expected


def test_list_field_with_large_lists():
    """Test ListField with large lists"""
    field = TextListField(name="BigList")
    large_list = [f"item{i}" for i in range(5)]  # Reduced to 5 for cleaner test

    result = field.contains_all(large_list)
    # Should generate an AND statement with 5 conditions
    assert result.startswith("AND(")
    assert result.endswith(")")
    # Count the number of FIND functions instead of commas since commas appear inside FIND functions too
    assert result.count("FIND(") == 5
