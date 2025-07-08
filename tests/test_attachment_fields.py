from airtableformulahelpers import AND, OR, AttachmentsField, Field


def test_attachments_field_is_not_empty():
    """Test AttachmentsField is_not_empty method"""
    field = AttachmentsField(name="Documents")
    result = field.is_not_empty()
    assert result == "LEN({Documents})>0"


def test_attachments_field_is_empty():
    """Test AttachmentsField is_empty method"""
    field = AttachmentsField(name="Documents")
    result = field.is_empty()
    assert result == "LEN({Documents})=0"


def test_attachments_field_count_is():
    """Test AttachmentsField count_is method"""
    field = AttachmentsField(name="Images")

    # Test with different counts
    assert field.count_is(1) == "LEN({Images})=1"
    assert field.count_is(5) == "LEN({Images})=5"
    assert field.count_is(0) == "LEN({Images})=0"


def test_attachments_field_overrides_base_methods():
    """Test AttachmentsField overrides base Field methods"""
    field = AttachmentsField(name="Files")

    # Test that is_empty and is_not_empty are overridden
    assert field.is_empty() == "LEN({Files})=0"
    assert field.is_not_empty() == "LEN({Files})>0"

    # Test that these are different from base Field methods
    base_field = Field(name="Files")
    assert field.is_empty() != base_field.is_empty()
    assert field.is_not_empty() != base_field.is_not_empty()


def test_attachments_field_inheritance():
    """Test AttachmentsField inherits from Field"""
    field = AttachmentsField(name="TestAttachments")

    # Test inherited name property
    assert field.name == "TestAttachments"


def test_attachments_field_with_different_names():
    """Test AttachmentsField with different field names"""
    fields = [
        AttachmentsField(name="Photos"),
        AttachmentsField(name="Supporting Documents"),
        AttachmentsField(name="file_uploads"),
        AttachmentsField(name="Media-Files"),
    ]

    for field in fields:
        assert field.is_empty() == f"LEN({{{field.name}}})=0"
        assert field.is_not_empty() == f"LEN({{{field.name}}})>0"
        assert field.count_is(3) == f"LEN({{{field.name}}})=3"


def test_attachments_field_in_logical_operations():
    """Test AttachmentsField in logical operations"""
    photos_field = AttachmentsField(name="Photos")
    docs_field = AttachmentsField(name="Documents")

    # Test with AND
    result = AND(photos_field.is_not_empty(), docs_field.count_is(2))
    assert result == "AND(LEN({Photos})>0,LEN({Documents})=2)"

    # Test with OR
    result = OR(photos_field.is_empty(), docs_field.is_empty())
    assert result == "OR(LEN({Photos})=0,LEN({Documents})=0)"


def test_attachments_field_count_variations():
    """Test AttachmentsField count_is with various numbers"""
    field = AttachmentsField(name="Attachments")

    # Test edge cases
    assert field.count_is(0) == "LEN({Attachments})=0"
    assert field.count_is(1) == "LEN({Attachments})=1"
    assert field.count_is(10) == "LEN({Attachments})=10"
    assert field.count_is(100) == "LEN({Attachments})=100"


def test_attachment_field_with_large_counts():
    """Test AttachmentsField with large counts"""
    field = AttachmentsField(name="ManyFiles")

    assert field.count_is(10000) == "LEN({ManyFiles})=10000"
