from airtableformulahelpers import (
    BooleanField,
    Field,
    NumberField,
    TextField,
    id_equals,
)


class TestID:
    """Tests for utility functions"""

    def test_id_equals(self):
        """Test id_equals function"""
        test_id = "rec123ABC"
        result = id_equals(test_id)
        assert result == f"RECORD_ID()='{test_id}'"

    def test_id_equals_with_special_characters(self):
        """Test id_equals with special characters"""
        test_id = "rec-123_ABC"
        result = id_equals(test_id)
        assert result == f"RECORD_ID()='{test_id}'"


class TestField:
    """Tests for the base Field class"""

    def test_field_is_empty(self):
        """Test field is_empty method"""
        field = Field(name="TestField")
        result = field.is_empty()
        assert result == "{TestField}=BLANK()"

    def test_field_is_not_empty(self):
        """Test field is_not_empty method"""
        field = Field(name="TestField")
        result = field.is_not_empty()
        assert result == "{TestField}"

    def test_field_with_spaces_in_name(self):
        """Test field with spaces in name"""
        field = Field(name="Test Field")
        assert field.is_empty() == "{Test Field}=BLANK()"
        assert field.is_not_empty() == "{Test Field}"

    def test_field_with_special_characters(self):
        """Test field with special characters in name"""
        field = Field(name="Test-Field_123")
        assert field.is_empty() == "{Test-Field_123}=BLANK()"
        assert field.is_not_empty() == "{Test-Field_123}"

    def test_field_name_property(self):
        """Test field name property"""
        field = Field(name="MyField")
        assert field.name == "MyField"

    def test_field_names_with_special_characters(self):
        """Test all field types with special characters in names"""
        special_names = [
            "Field Name",  # spaces
            "Field-Name",  # hyphens
            "Field_Name",  # underscores
            "Field123",  # numbers
            "Field.Name",  # dots
            "Field(1)",  # parentheses
        ]

        for name in special_names:
            # Test all field types handle special characters
            text_field = TextField(name=name)
            bool_field = BooleanField(name=name)
            number_field = NumberField(name=name)

            assert text_field.equals("test") == f'{{{name}}}="test"'
            assert bool_field.is_true() == f"{{{name}}}=TRUE()"
            assert number_field.equals(1) == f"{{{name}}}=1"

    def test_empty_field_names(self):
        """Test fields with empty names"""
        field = Field(name="")
        assert field.is_empty() == "{}=BLANK()"
        assert field.is_not_empty() == "{}"
