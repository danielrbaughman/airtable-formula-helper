from airtableformulahelpers import (
    AND,
    IF,
    NOT,
    OR,
    AttachmentsField,
    BooleanField,
    NumberField,
    TextField,
)


def test_if_then_else_basic():
    """Test basic IF/THEN/ELSE construction"""
    result = IF("condition").THEN("true_value").ELSE("false_value")
    assert result == "IF(condition, true_value, false_value)"


def test_if_then_else_with_field_conditions():
    """Test IF/THEN/ELSE with field conditions"""
    status_field = TextField(name="Status")
    result = IF(status_field.equals("Active")).THEN("Show").ELSE("Hide")
    assert result == 'IF({Status}="Active", Show, Hide)'


def test_if_then_else_with_complex_conditions():
    """Test IF/THEN/ELSE with complex conditions"""
    name_field = TextField(name="Name")
    active_field = BooleanField(name="Active")

    condition = AND(name_field.not_equals(""), active_field.is_true())

    result = IF(condition).THEN("Valid").ELSE("Invalid")
    assert result == 'IF(AND({Name}!="",{Active}=TRUE()), Valid, Invalid)'


def test_if_then_else_nested():
    """Test nested IF statements"""
    score_field = NumberField(name="Score")

    inner_if = IF(score_field.greater_than(90)).THEN("A").ELSE("B")
    outer_if = IF(score_field.greater_than(95)).THEN("A+").ELSE(inner_if)

    assert outer_if == "IF({Score}>95, A+, IF({Score}>90, A, B))"


def test_if_with_logical_functions():
    """Test IF with various logical functions"""
    field1 = TextField(name="Field1")
    field2 = TextField(name="Field2")

    # Test with OR
    result = IF(OR(field1.equals("A"), field2.equals("B"))).THEN("Pass").ELSE("Fail")
    assert result == 'IF(OR({Field1}="A",{Field2}="B"), Pass, Fail)'

    # Test with NOT
    result = IF(NOT(field1.is_empty())).THEN("Has Value").ELSE("Empty")
    assert result == "IF(NOT({Field1}=BLANK()), Has Value, Empty)"


def test_if_then_else_with_all_field_types():
    """Test IF/THEN/ELSE with all field types"""
    text_field = TextField(name="Status")
    bool_field = BooleanField(name="Active")
    number_field = NumberField(name="Count")
    attachment_field = AttachmentsField(name="Files")

    # Complex condition using all field types
    condition = AND(
        text_field.equals("Published"),
        bool_field.is_true(),
        number_field.greater_than(0),
        attachment_field.is_not_empty(),
    )

    result = IF(condition).THEN("Valid").ELSE("Invalid")
    expected = (
        'IF(AND({Status}="Published",{Active}=TRUE(),{Count}>0,LEN({Files})>0), Valid, Invalid)'
    )
    assert result == expected
