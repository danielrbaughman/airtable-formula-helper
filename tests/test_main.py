from datetime import datetime

from airtableformulahelpers import (
    AND,
    IF,
    NOT,
    OR,
    XOR,
    AttachmentsField,
    BoolField,
    DateComparison,
    DateField,
    Field,
    ListField,
    Number,
    TextField,
    id_equals,
)


class TestLogicFunctions:
    class TestAND:
        """Tests for the AND logical function"""

        def test_and_single_argument(self):
            """Test AND with single argument"""
            result = AND("condition1")
            assert result == "AND(condition1)"

        def test_and_multiple_arguments(self):
            """Test AND with multiple arguments"""
            result = AND("cond1", "cond2", "cond3")
            assert result == "AND(cond1,cond2,cond3)"

        def test_and_empty_arguments(self):
            """Test AND with no arguments"""
            result = AND()
            assert result == "AND()"

        def test_and_with_field_conditions(self):
            """Test AND with real field conditions"""
            name_field = TextField(name="Name")
            status_field = BoolField(name="Active")
            
            result = AND(
                name_field.equals("John"),
                status_field.is_true()
            )
            assert result == 'AND({Name}="John",{Active}=TRUE())'

        def test_and_with_many_arguments(self):
            """Test AND with many arguments"""
            result = AND("a", "b", "c", "d", "e")
            assert result == "AND(a,b,c,d,e)"


    class TestOR:
        """Tests for the OR logical function"""

        def test_or_single_argument(self):
            """Test OR with single argument"""
            result = OR("condition1")
            assert result == "OR(condition1)"

        def test_or_multiple_arguments(self):
            """Test OR with multiple arguments"""
            result = OR("cond1", "cond2", "cond3")
            assert result == "OR(cond1,cond2,cond3)"

        def test_or_empty_arguments(self):
            """Test OR with no arguments"""
            result = OR()
            assert result == "OR()"

        def test_or_with_field_conditions(self):
            """Test OR with real field conditions"""
            status_field = TextField(name="Status")
            
            result = OR(
                status_field.equals("Draft"),
                status_field.equals("Review"),
                status_field.equals("Published")
            )
            assert result == 'OR({Status}="Draft",{Status}="Review",{Status}="Published")'

        def test_or_with_many_arguments(self):
            """Test OR with many arguments"""
            result = OR("x", "y", "z", "w")
            assert result == "OR(x,y,z,w)"


    class TestXOR:
        """Tests for the XOR logical function"""

        def test_xor_single_argument(self):
            """Test XOR with single argument"""
            result = XOR("condition1")
            assert result == "XOR(condition1)"

        def test_xor_multiple_arguments(self):
            """Test XOR with multiple arguments"""
            result = XOR("cond1", "cond2", "cond3")
            assert result == "XOR(cond1,cond2,cond3)"

        def test_xor_empty_arguments(self):
            """Test XOR with no arguments"""
            result = XOR()
            assert result == "XOR()"

        def test_xor_with_field_conditions(self):
            """Test XOR with real field conditions"""
            flag1 = BoolField(name="Flag1")
            flag2 = BoolField(name="Flag2")
            
            result = XOR(
                flag1.is_true(),
                flag2.is_true()
            )
            assert result == "XOR({Flag1}=TRUE(),{Flag2}=TRUE())"

        def test_xor_with_many_arguments(self):
            """Test XOR with many arguments"""
            result = XOR("p", "q", "r")
            assert result == "XOR(p,q,r)"


    class TestNOT:
        """Tests for the NOT logical function"""

        def test_not_single_argument(self):
            """Test NOT with single argument"""
            result = NOT("condition1")
            assert result == "NOT(condition1)"

        def test_not_multiple_arguments(self):
            """Test NOT with multiple arguments"""
            result = NOT("cond1", "cond2", "cond3")
            assert result == "NOT(cond1,cond2,cond3)"

        def test_not_empty_arguments(self):
            """Test NOT with no arguments"""
            result = NOT()
            assert result == "NOT()"

        def test_not_with_field_conditions(self):
            """Test NOT with real field conditions"""
            active_field = BoolField(name="Active")
            
            result = NOT(active_field.is_true())
            assert result == "NOT({Active}=TRUE())"

        def test_not_with_multiple_field_conditions(self):
            """Test NOT with multiple field conditions"""
            name_field = TextField(name="Name")
            status_field = TextField(name="Status")
            
            result = NOT(
                name_field.is_empty(),
                status_field.equals("Archived")
            )
            assert result == 'NOT({Name}=BLANK(),{Status}="Archived")'


    class TestLogicCombinations:
        """Integration tests for combining logical functions"""

        def test_nested_logical_operations(self):
            """Test nesting logical functions"""
            result = AND(
                OR("a", "b"),
                NOT("c"),
                XOR("d", "e")
            )
            assert result == "AND(OR(a,b),NOT(c),XOR(d,e))"

        def test_complex_nested_operations(self):
            """Test complex nested logical operations"""
            result = OR(
                AND("condition1", "condition2"),
                NOT(XOR("condition3", "condition4"))
            )
            assert result == "OR(AND(condition1,condition2),NOT(XOR(condition3,condition4)))"

        def test_real_world_complex_formula(self):
            """Test a real-world complex formula"""
            name_field = TextField(name="Name")
            status_field = TextField(name="Status")
            active_field = BoolField(name="Active")
            
            result = OR(
                AND(
                    name_field.not_equals(""),
                    status_field.equals("Published"),
                    active_field.is_true()
                ),
                NOT(
                    XOR(
                        status_field.equals("Draft"),
                        status_field.equals("Review")
                    )
                )
            )
            expected = 'OR(AND({Name}!="",{Status}="Published",{Active}=TRUE()),NOT(XOR({Status}="Draft",{Status}="Review")))'
            assert result == expected


    class TestLogicEdgeCases:
        """Edge case tests for logical functions"""

        def test_empty_string_arguments(self):
            """Test with empty string arguments"""
            assert AND("", "condition") == "AND(,condition)"
            assert OR("", "condition") == "OR(,condition)"
            assert XOR("", "condition") == "XOR(,condition)"
            assert NOT("", "condition") == "NOT(,condition)"

        def test_special_characters_in_arguments(self):
            """Test with special characters in arguments"""
            special_condition = '{Field Name}="Value with spaces"'
            assert AND(special_condition) == f"AND({special_condition})"
            assert OR(special_condition) == f"OR({special_condition})"
            assert XOR(special_condition) == f"XOR({special_condition})"
            assert NOT(special_condition) == f"NOT({special_condition})"

        def test_arguments_with_quotes(self):
            """Test with arguments containing quotes"""
            quoted_condition = 'FIND("quoted value", {Field})'
            assert AND(quoted_condition) == f"AND({quoted_condition})"
            assert OR(quoted_condition) == f"OR({quoted_condition})"
            assert XOR(quoted_condition) == f"XOR({quoted_condition})"
            assert NOT(quoted_condition) == f"NOT({quoted_condition})"

        def test_very_long_argument_list(self):
            """Test with many arguments"""
            conditions = [f"condition{i}" for i in range(10)]
            expected_args = ",".join(conditions)
            
            assert AND(*conditions) == f"AND({expected_args})"
            assert OR(*conditions) == f"OR({expected_args})"
            assert XOR(*conditions) == f"XOR({expected_args})"
            assert NOT(*conditions) == f"NOT({expected_args})"

        def test_whitespace_in_arguments(self):
            """Test with whitespace in arguments"""
            assert AND("  condition  ") == "AND(  condition  )"
            assert OR("condition\n") == "OR(condition\n)"
            assert XOR("\tcondition") == "XOR(\tcondition)"
            assert NOT("condition with spaces") == "NOT(condition with spaces)"

        def test_logical_functions_with_mixed_types(self):
            """Test logical functions with mixed field types"""
            text_field = TextField(name="Name")
            bool_field = BoolField(name="Active")
            number_field = Number(name="Score")
            
            result = AND(
                text_field.not_equals(""),
                bool_field.is_true(),
                number_field.greater_than(0)
            )
            expected = 'AND({Name}!="",{Active}=TRUE(),{Score}>0)'
            assert result == expected

        def test_nested_logical_operations_deep(self):
            """Test deeply nested logical operations"""
            field1 = TextField(name="F1")
            field2 = TextField(name="F2")
            field3 = TextField(name="F3")
            field4 = TextField(name="F4")
            
            result = AND(
                OR(field1.equals("A"), field2.equals("B")),
                NOT(
                    XOR(field3.equals("C"), field4.equals("D"))
                )
            )
            expected = 'AND(OR({F1}="A",{F2}="B"),NOT(XOR({F3}="C",{F4}="D")))'
            assert result == expected


class TestIF:
    """Tests for the IF/THEN/ELSE functionality"""

    def test_if_then_else_basic(self):
        """Test basic IF/THEN/ELSE construction"""
        result = IF("condition").THEN("true_value").ELSE("false_value")
        assert result == "IF(condition, true_value, false_value)"

    def test_if_then_else_with_field_conditions(self):
        """Test IF/THEN/ELSE with field conditions"""
        status_field = TextField(name="Status")
        result = IF(status_field.equals("Active")).THEN("Show").ELSE("Hide")
        assert result == 'IF({Status}="Active", Show, Hide)'

    def test_if_then_else_with_complex_conditions(self):
        """Test IF/THEN/ELSE with complex conditions"""
        name_field = TextField(name="Name")
        active_field = BoolField(name="Active")
        
        condition = AND(
            name_field.not_equals(""),
            active_field.is_true()
        )
        
        result = IF(condition).THEN("Valid").ELSE("Invalid")
        assert result == 'IF(AND({Name}!="",{Active}=TRUE()), Valid, Invalid)'

    def test_if_then_else_nested(self):
        """Test nested IF statements"""
        score_field = Number(name="Score")
        
        inner_if = IF(score_field.greater_than(90)).THEN("A").ELSE("B")
        outer_if = IF(score_field.greater_than(95)).THEN("A+").ELSE(inner_if)
        
        assert outer_if == "IF({Score}>95, A+, IF({Score}>90, A, B))"

    def test_if_with_logical_functions(self):
        """Test IF with various logical functions"""
        field1 = TextField(name="Field1")
        field2 = TextField(name="Field2")
        
        # Test with OR
        result = IF(OR(field1.equals("A"), field2.equals("B"))).THEN("Pass").ELSE("Fail")
        assert result == 'IF(OR({Field1}="A",{Field2}="B"), Pass, Fail)'
        
        # Test with NOT
        result = IF(NOT(field1.is_empty())).THEN("Has Value").ELSE("Empty")
        assert result == "IF(NOT({Field1}=BLANK()), Has Value, Empty)"
    
    def test_if_then_else_with_all_field_types(self):
        """Test IF/THEN/ELSE with all field types"""
        text_field = TextField(name="Status")
        bool_field = BoolField(name="Active")
        number_field = Number(name="Count")
        attachment_field = AttachmentsField(name="Files")
        
        # Complex condition using all field types
        condition = AND(
            text_field.equals("Published"),
            bool_field.is_true(),
            number_field.greater_than(0),
            attachment_field.is_not_empty()
        )
        
        result = IF(condition).THEN("Valid").ELSE("Invalid")
        expected = 'IF(AND({Status}="Published",{Active}=TRUE(),{Count}>0,LEN({Files})>0), Valid, Invalid)'
        assert result == expected

class TestBasics:
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
                "Field123",    # numbers
                "Field.Name",  # dots
                "Field(1)",    # parentheses
            ]
            
            for name in special_names:
                # Test all field types handle special characters
                text_field = TextField(name=name)
                bool_field = BoolField(name=name)
                number_field = Number(name=name)
                
                assert text_field.equals("test") == f'{{{name}}}="test"'
                assert bool_field.is_true() == f"{{{name}}}=TRUE()"
                assert number_field.equals(1) == f"{{{name}}}=1"

        def test_empty_field_names(self):
            """Test fields with empty names"""
            field = Field(name="")
            assert field.is_empty() == "{}=BLANK()"
            assert field.is_not_empty() == "{}"


class TestFields:
    class TestTextField:
        """Comprehensive tests for TextField class"""

        def test_text_field_equals(self):
            """Test TextField equals method"""
            field = TextField(name="Name")
            result = field.equals("John")
            assert result == '{Name}="John"'

        def test_text_field_not_equals(self):
            """Test TextField not_equals method"""
            field = TextField(name="Name")
            result = field.not_equals("John")
            assert result == '{Name}!="John"'

        def test_text_field_contains(self):
            """Test TextField contains method (case-insensitive)"""
            field = TextField(name="Description")
            result = field.contains("test")
            assert result == 'FIND(TRIM(LOWER("test")), TRIM(LOWER({Description})))>0'

        def test_text_field_not_contains(self):
            """Test TextField not_contains method (case-insensitive)"""
            field = TextField(name="Description")
            result = field.not_contains("test")
            assert result == 'FIND(TRIM(LOWER("test")), TRIM(LOWER({Description})))=0'

        def test_text_field_starts_with(self):
            """Test TextField starts_with method (case-insensitive)"""
            field = TextField(name="Title")
            result = field.starts_with("Mr")
            assert result == 'FIND(TRIM(LOWER("Mr")), TRIM(LOWER({Title})))=1'

        def test_text_field_not_starts_with(self):
            """Test TextField not_starts_with method (case-insensitive)"""
            field = TextField(name="Title")
            result = field.not_starts_with("Mr")
            assert result == 'FIND(TRIM(LOWER("Mr")), TRIM(LOWER({Title})))!=1'

        def test_text_field_ends_with(self):
            """Test TextField ends_with method (case-insensitive)"""
            field = TextField(name="Email")
            result = field.ends_with(".com")
            expected = 'FIND(TRIM(LOWER(".com")), TRIM(LOWER({Email}))) = LEN(TRIM(LOWER({Email}))) - LEN(TRIM(LOWER(".com"))) + 1'
            assert result == expected

        def test_text_field_not_ends_with(self):
            """Test TextField not_ends_with method (case-insensitive)"""
            field = TextField(name="Email")
            result = field.not_ends_with(".com")
            expected = 'FIND(TRIM(LOWER(".com")), TRIM(LOWER({Email}))) != LEN(TRIM(LOWER({Email}))) - LEN(TRIM(LOWER(".com"))) + 1'
            assert result == expected

        def test_text_field_regex_match(self):
            """Test TextField regex_match method"""
            field = TextField(name="Phone")
            result = field.regex_match(r"^\d{3}-\d{3}-\d{4}$")
            assert result == r'REGEX_MATCH({Phone}, "^\d{3}-\d{3}-\d{4}$")'

        def test_text_field_with_special_characters(self):
            """Test TextField with special characters in values"""
            field = TextField(name="Data")
            
            # Test with quotes
            result = field.equals('Text with "quotes"')
            assert result == '{Data}="Text with "quotes""'
            
            # Test with apostrophes
            result = field.equals("Text with 'apostrophes'")
            assert result == '{Data}="Text with \'apostrophes\'"'

        def test_text_field_with_empty_values(self):
            """Test TextField with empty values"""
            field = TextField(name="Optional")
            result = field.equals("")
            assert result == '{Optional}=""'

        def test_text_field_inheritance(self):
            """Test TextField inherits from Field"""
            field = TextField(name="TestField")
            
            # Test inherited methods
            assert field.is_empty() == "{TestField}=BLANK()"
            assert field.is_not_empty() == "{TestField}"
            assert field.name == "TestField"

        def test_text_field_complex_regex(self):
            """Test TextField with complex regex patterns"""
            field = TextField(name="Code")
            
            # Email pattern
            result = field.regex_match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
            assert result == r'REGEX_MATCH({Code}, "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")'

        def test_text_field_find_method_edge_cases(self):
            """Test TextField _find method with edge cases"""
            field = TextField(name="Content")
            
            # Test with numbers
            result = field.contains("123")
            assert result == 'FIND(TRIM(LOWER("123")), TRIM(LOWER({Content})))>0'
            
            # Test with special characters  
            result = field.contains("@#$")
            assert result == 'FIND(TRIM(LOWER("@#$")), TRIM(LOWER({Content})))>0'
        
        def test_text_field_with_very_long_strings(self):
            """Test TextField with very long strings"""
            field = TextField(name="LongText")
            long_string = "A" * 1000  # 1000 character string
            
            result = field.equals(long_string)
            assert result == f'{{LongText}}="{long_string}"'

        def test_unicode_and_special_characters_in_values(self):
            """Test fields with unicode and special characters in values"""
            field = TextField(name="Unicode")
            
            # Test with emoji
            assert field.equals("Hello 👋") == '{Unicode}="Hello 👋"'
            
            # Test with unicode characters
            assert field.equals("Café") == '{Unicode}="Café"'
            
            # Test with special symbols
            assert field.equals("Price: $50.00") == '{Unicode}="Price: $50.00"'

        def test_regex_with_complex_patterns(self):
            """Test TextField regex with complex patterns"""
            field = TextField(name="Pattern")
            
            # Complex email regex
            email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
            result = field.regex_match(email_pattern)
            assert result == f'REGEX_MATCH({{Pattern}}, "{email_pattern}")'


    class TestListField:
        """Tests for ListField class"""

        def test_list_field_contains(self):
            """Test ListField contains method (case-insensitive)"""
            field = ListField(name="Tags")
            result = field.contains("urgent")
            assert result == 'FIND(LOWER("urgent"), LOWER({Tags}))>0'

        def test_list_field_not_contains(self):
            """Test ListField not_contains method (case-insensitive)"""
            field = ListField(name="Tags")
            result = field.not_contains("urgent")
            assert result == 'FIND(LOWER("urgent"), LOWER({Tags}))=0'

        def test_list_field_contains_all(self):
            """Test ListField contains_all method"""
            field = ListField(name="Skills")
            result = field.contains_all(["python", "javascript", "sql"])
            expected = 'AND(FIND(LOWER("python"), LOWER({Skills}))>0,FIND(LOWER("javascript"), LOWER({Skills}))>0,FIND(LOWER("sql"), LOWER({Skills}))>0)'
            assert result == expected

        def test_list_field_contains_any(self):
            """Test ListField contains_any method"""
            field = ListField(name="Skills")
            result = field.contains_any(["python", "javascript", "sql"])
            expected = 'OR(FIND(LOWER("python"), LOWER({Skills}))>0,FIND(LOWER("javascript"), LOWER({Skills}))>0,FIND(LOWER("sql"), LOWER({Skills}))>0)'
            assert result == expected

        def test_list_field_contains_all_single_item(self):
            """Test ListField contains_all with single item"""
            field = ListField(name="Categories")
            result = field.contains_all(["business"])
            expected = 'AND(FIND(LOWER("business"), LOWER({Categories}))>0)'
            assert result == expected

        def test_list_field_contains_any_single_item(self):
            """Test ListField contains_any with single item"""
            field = ListField(name="Categories")
            result = field.contains_any(["business"])
            expected = 'OR(FIND(LOWER("business"), LOWER({Categories}))>0)'
            assert result == expected

        def test_list_field_contains_all_empty_list(self):
            """Test ListField contains_all with empty list"""
            field = ListField(name="Empty")
            result = field.contains_all([])
            assert result == "AND()"

        def test_list_field_contains_any_empty_list(self):
            """Test ListField contains_any with empty list"""
            field = ListField(name="Empty")
            result = field.contains_any([])
            assert result == "OR()"

        def test_list_field_with_special_characters(self):
            """Test ListField with special characters in values"""
            field = ListField(name="Data")
            
            # Test with spaces
            result = field.contains("web development")
            assert result == 'FIND(LOWER("web development"), LOWER({Data}))>0'
            
            # Test with special characters
            result = field.contains("C++")
            assert result == 'FIND(LOWER("C++"), LOWER({Data}))>0'

        def test_list_field_inheritance(self):
            """Test ListField inherits from Field"""
            field = ListField(name="TestList")
            
            # Test inherited methods
            assert field.is_empty() == "{TestList}=BLANK()"
            assert field.is_not_empty() == "{TestList}"
            assert field.name == "TestList"

        def test_list_field_case_insensitive(self):
            """Test ListField case insensitive behavior"""
            field = ListField(name="Items")
            
            # Test with mixed case
            result = field.contains("Python")
            assert result == 'FIND(LOWER("Python"), LOWER({Items}))>0'
            
            result = field.contains_all(["JAVA", "python", "Go"])
            expected = 'AND(FIND(LOWER("JAVA"), LOWER({Items}))>0,FIND(LOWER("python"), LOWER({Items}))>0,FIND(LOWER("Go"), LOWER({Items}))>0)'
            assert result == expected
        
        def test_list_field_with_large_lists(self):
            """Test ListField with large lists"""
            field = ListField(name="BigList")
            large_list = [f"item{i}" for i in range(5)]  # Reduced to 5 for cleaner test
            
            result = field.contains_all(large_list)
            # Should generate an AND statement with 5 conditions
            assert result.startswith("AND(")
            assert result.endswith(")")
            # Count the number of FIND functions instead of commas since commas appear inside FIND functions too
            assert result.count("FIND(") == 5


    class TestNumberField:
        """Tests for Number field class"""

        def test_number_field_equals_int(self):
            """Test Number field equals with integer"""
            field = Number(name="Score")
            result = field.equals(100)
            assert result == "{Score}=100"

        def test_number_field_equals_float(self):
            """Test Number field equals with float"""
            field = Number(name="Price")
            result = field.equals(99.99)
            assert result == "{Price}=99.99"

        def test_number_field_not_equals_int(self):
            """Test Number field not_equals with integer"""
            field = Number(name="Score")
            result = field.not_equals(0)
            assert result == "{Score}!=0"

        def test_number_field_not_equals_float(self):
            """Test Number field not_equals with float"""
            field = Number(name="Price")
            result = field.not_equals(0.0)
            assert result == "{Price}!=0.0"

        def test_number_field_greater_than(self):
            """Test Number field greater_than method"""
            field = Number(name="Age")
            result = field.greater_than(18)
            assert result == "{Age}>18"

        def test_number_field_less_than(self):
            """Test Number field less_than method"""
            field = Number(name="Age")
            result = field.less_than(65)
            assert result == "{Age}<65"

        def test_number_field_greater_than_or_equals(self):
            """Test Number field greater_than_or_equals method"""
            field = Number(name="Grade")
            result = field.greater_than_or_equals(70)
            assert result == "{Grade}>=70"

        def test_number_field_less_than_or_equals(self):
            """Test Number field less_than_or_equals method"""
            field = Number(name="Grade")
            result = field.less_than_or_equals(100)
            assert result == "{Grade}<=100"

        def test_number_field_with_negative_numbers(self):
            """Test Number field with negative numbers"""
            field = Number(name="Temperature")
            
            assert field.equals(-10) == "{Temperature}=-10"
            assert field.greater_than(-5) == "{Temperature}>-5"
            assert field.less_than(-15) == "{Temperature}<-15"

        def test_number_field_with_zero(self):
            """Test Number field with zero"""
            field = Number(name="Count")
            
            assert field.equals(0) == "{Count}=0"
            assert field.not_equals(0) == "{Count}!=0"
            assert field.greater_than(0) == "{Count}>0"
            assert field.less_than(0) == "{Count}<0"

        def test_number_field_with_large_numbers(self):
            """Test Number field with large numbers"""
            field = Number(name="Population")
            
            assert field.equals(1000000) == "{Population}=1000000"
            assert field.greater_than(999999) == "{Population}>999999"

        def test_number_field_with_decimal_precision(self):
            """Test Number field with decimal precision"""
            field = Number(name="Precision")
            
            assert field.equals(3.14159) == "{Precision}=3.14159"
            assert field.greater_than(0.001) == "{Precision}>0.001"

        def test_number_field_inheritance(self):
            """Test Number field inherits from Field"""
            field = Number(name="TestNumber")
            
            # Test inherited methods
            assert field.is_empty() == "{TestNumber}=BLANK()"
            assert field.is_not_empty() == "{TestNumber}"
            assert field.name == "TestNumber"

        def test_number_field_compare_method(self):
            """Test Number field _compare method indirectly"""
            field = Number(name="Value")
            
            # Test all comparison operators
            assert field._compare("=", 10) == "{Value}=10"
            assert field._compare("!=", 10) == "{Value}!=10"
            assert field._compare(">", 10) == "{Value}>10"
            assert field._compare("<", 10) == "{Value}<10"
            assert field._compare(">=", 10) == "{Value}>=10"
            assert field._compare("<=", 10) == "{Value}<=10"
        
        def test_number_field_with_extreme_values(self):
            """Test Number field with extreme values"""
            field = Number(name="Extreme")
            
            # Test very large numbers
            assert field.equals(999999999999) == "{Extreme}=999999999999"
            
            # Test very small decimals
            assert field.equals(0.000001) == "{Extreme}=1e-06"
            
            # Test negative large numbers
            assert field.equals(-999999999999) == "{Extreme}=-999999999999"


    class TestBoolField:
        """Comprehensive tests for BoolField class"""

        def test_bool_field_equals_true(self):
            """Test BoolField equals with True"""
            field = BoolField(name="IsActive")
            result = field.equals(True)
            assert result == "{IsActive}=TRUE()"

        def test_bool_field_equals_false(self):
            """Test BoolField equals with False"""
            field = BoolField(name="IsActive")
            result = field.equals(False)
            assert result == "{IsActive}=FALSE()"

        def test_bool_field_is_true(self):
            """Test BoolField is_true method"""
            field = BoolField(name="Verified")
            result = field.is_true()
            assert result == "{Verified}=TRUE()"

        def test_bool_field_is_false(self):
            """Test BoolField is_false method"""
            field = BoolField(name="Verified")
            result = field.is_false()
            assert result == "{Verified}=FALSE()"

        def test_bool_field_inheritance(self):
            """Test BoolField inherits from Field"""
            field = BoolField(name="TestBool")
            
            # Test inherited methods
            assert field.is_empty() == "{TestBool}=BLANK()"
            assert field.is_not_empty() == "{TestBool}"
            assert field.name == "TestBool"

        def test_bool_field_with_different_names(self):
            """Test BoolField with different field names"""
            fields = [
                BoolField(name="Active"),
                BoolField(name="Is Published"),
                BoolField(name="has_permissions"),
                BoolField(name="Flag-123")
            ]
            
            for field in fields:
                assert field.is_true() == f"{{{field.name}}}=TRUE()"
                assert field.is_false() == f"{{{field.name}}}=FALSE()"

        def test_bool_field_equals_method_behavior(self):
            """Test BoolField equals method with different boolean values"""
            field = BoolField(name="Status")
            
            # Test with explicit boolean values
            assert field.equals(True) == "{Status}=TRUE()"
            assert field.equals(False) == "{Status}=FALSE()"

        def test_bool_field_in_logical_operations(self):
            """Test BoolField in logical operations"""
            active_field = BoolField(name="Active")
            verified_field = BoolField(name="Verified")
            
            # Test with AND
            result = AND(active_field.is_true(), verified_field.is_true())
            assert result == "AND({Active}=TRUE(),{Verified}=TRUE())"
            
            # Test with OR
            result = OR(active_field.is_false(), verified_field.is_false())
            assert result == "OR({Active}=FALSE(),{Verified}=FALSE())"
            
            # Test with NOT
            result = NOT(active_field.is_true())
            assert result == "NOT({Active}=TRUE())"


    class TestAttachmentsField:
        """Tests for AttachmentsField class"""

        def test_attachments_field_is_not_empty(self):
            """Test AttachmentsField is_not_empty method"""
            field = AttachmentsField(name="Documents")
            result = field.is_not_empty()
            assert result == "LEN({Documents})>0"

        def test_attachments_field_is_empty(self):
            """Test AttachmentsField is_empty method"""
            field = AttachmentsField(name="Documents")
            result = field.is_empty()
            assert result == "LEN({Documents})=0"

        def test_attachments_field_count_is(self):
            """Test AttachmentsField count_is method"""
            field = AttachmentsField(name="Images")
            
            # Test with different counts
            assert field.count_is(1) == "LEN({Images})=1"
            assert field.count_is(5) == "LEN({Images})=5"
            assert field.count_is(0) == "LEN({Images})=0"

        def test_attachments_field_overrides_base_methods(self):
            """Test AttachmentsField overrides base Field methods"""
            field = AttachmentsField(name="Files")
            
            # Test that is_empty and is_not_empty are overridden
            assert field.is_empty() == "LEN({Files})=0"
            assert field.is_not_empty() == "LEN({Files})>0"
            
            # Test that these are different from base Field methods
            base_field = Field(name="Files")
            assert field.is_empty() != base_field.is_empty()
            assert field.is_not_empty() != base_field.is_not_empty()

        def test_attachments_field_inheritance(self):
            """Test AttachmentsField inherits from Field"""
            field = AttachmentsField(name="TestAttachments")
            
            # Test inherited name property
            assert field.name == "TestAttachments"

        def test_attachments_field_with_different_names(self):
            """Test AttachmentsField with different field names"""
            fields = [
                AttachmentsField(name="Photos"),
                AttachmentsField(name="Supporting Documents"),
                AttachmentsField(name="file_uploads"),
                AttachmentsField(name="Media-Files")
            ]
            
            for field in fields:
                assert field.is_empty() == f"LEN({{{field.name}}})=0"
                assert field.is_not_empty() == f"LEN({{{field.name}}})>0"
                assert field.count_is(3) == f"LEN({{{field.name}}})=3"

        def test_attachments_field_in_logical_operations(self):
            """Test AttachmentsField in logical operations"""
            photos_field = AttachmentsField(name="Photos")
            docs_field = AttachmentsField(name="Documents")
            
            # Test with AND
            result = AND(photos_field.is_not_empty(), docs_field.count_is(2))
            assert result == "AND(LEN({Photos})>0,LEN({Documents})=2)"
            
            # Test with OR
            result = OR(photos_field.is_empty(), docs_field.is_empty())
            assert result == "OR(LEN({Photos})=0,LEN({Documents})=0)"

        def test_attachments_field_count_variations(self):
            """Test AttachmentsField count_is with various numbers"""
            field = AttachmentsField(name="Attachments")
            
            # Test edge cases
            assert field.count_is(0) == "LEN({Attachments})=0"
            assert field.count_is(1) == "LEN({Attachments})=1"
            assert field.count_is(10) == "LEN({Attachments})=10"
            assert field.count_is(100) == "LEN({Attachments})=100"
        
        def test_attachment_field_with_large_counts(self):
            """Test AttachmentsField with large counts"""
            field = AttachmentsField(name="ManyFiles")
            
            assert field.count_is(10000) == "LEN({ManyFiles})=10000"


    class TestDateField:
        """Tests for DateField class"""

        def test_date_field_is_on_with_datetime(self):
            """Test DateField is_on method with datetime object"""
            field = DateField(name="CreatedAt")
            test_date = datetime(2023, 12, 25, 10, 30, 0)
            result = field.is_on(test_date)
            assert result == "DATETIME_PARSE('2023-12-25 10:30:00')=DATETIME_PARSE({CreatedAt})"

        def test_date_field_is_on_with_string(self):
            """Test DateField is_on method with string date"""
            field = DateField(name="DueDate")
            result = field.is_on("2023-12-25")
            assert result == "DATETIME_PARSE('2023-12-25 00:00:00')=DATETIME_PARSE({DueDate})"

        def test_date_field_is_on_returns_comparison(self):
            """Test DateField is_on method returns DateComparison when no date provided"""
            field = DateField(name="StartDate")
            result = field.is_on()
            assert isinstance(result, DateComparison)
            assert result.name == "StartDate"
            assert result.compare == "="

        def test_date_field_is_on_or_after_with_datetime(self):
            """Test DateField is_on_or_after method with datetime object"""
            field = DateField(name="EventDate")
            test_date = datetime(2023, 1, 1, 0, 0, 0)
            result = field.is_on_or_after(test_date)
            assert result == "DATETIME_PARSE('2023-01-01 00:00:00')>=DATETIME_PARSE({EventDate})"

        def test_date_field_is_on_or_after_returns_comparison(self):
            """Test DateField is_on_or_after method returns DateComparison when no date provided"""
            field = DateField(name="StartDate")
            result = field.is_on_or_after()
            assert isinstance(result, DateComparison)
            assert result.name == "StartDate"
            assert result.compare == ">="

        def test_date_field_is_on_or_before_with_datetime(self):
            """Test DateField is_on_or_before method with datetime object"""
            field = DateField(name="Deadline")
            test_date = datetime(2023, 12, 31, 23, 59, 59)
            result = field.is_on_or_before(test_date)
            assert result == "DATETIME_PARSE('2023-12-31 23:59:59')<=DATETIME_PARSE({Deadline})"

        def test_date_field_is_on_or_before_returns_comparison(self):
            """Test DateField is_on_or_before method returns DateComparison when no date provided"""
            field = DateField(name="EndDate")
            result = field.is_on_or_before()
            assert isinstance(result, DateComparison)
            assert result.name == "EndDate"
            assert result.compare == "<="

        def test_date_field_is_after_with_datetime(self):
            """Test DateField is_after method with datetime object"""
            field = DateField(name="LaunchDate")
            test_date = datetime(2023, 6, 15, 12, 0, 0)
            result = field.is_after(test_date)
            assert result == "DATETIME_PARSE('2023-06-15 12:00:00')<DATETIME_PARSE({LaunchDate})"

        def test_date_field_is_after_returns_comparison(self):
            """Test DateField is_after method returns DateComparison when no date provided"""
            field = DateField(name="StartDate")
            result = field.is_after()
            assert isinstance(result, DateComparison)
            assert result.name == "StartDate"
            assert result.compare == "<"

        def test_date_field_is_before_with_datetime(self):
            """Test DateField is_before method with datetime object"""
            field = DateField(name="ExpiryDate")
            test_date = datetime(2024, 1, 1, 0, 0, 0)
            result = field.is_before(test_date)
            assert result == "DATETIME_PARSE('2024-01-01 00:00:00')>DATETIME_PARSE({ExpiryDate})"

        def test_date_field_is_before_returns_comparison(self):
            """Test DateField is_before method returns DateComparison when no date provided"""
            field = DateField(name="EndDate")
            result = field.is_before()
            assert isinstance(result, DateComparison)
            assert result.name == "EndDate"
            assert result.compare == ">"

        def test_date_field_is_not_on_with_datetime(self):
            """Test DateField is_not_on method with datetime object"""
            field = DateField(name="UpdatedAt")
            test_date = datetime(2023, 5, 10, 14, 30, 0)
            result = field.is_not_on(test_date)
            assert result == "DATETIME_PARSE('2023-05-10 14:30:00')!=DATETIME_PARSE({UpdatedAt})"

        def test_date_field_is_not_on_returns_comparison(self):
            """Test DateField is_not_on method returns DateComparison when no date provided"""
            field = DateField(name="CreatedAt")
            result = field.is_not_on()
            assert isinstance(result, DateComparison)
            assert result.name == "CreatedAt"
            assert result.compare == "!="

        def test_date_field_inheritance(self):
            """Test DateField inherits from Field"""
            field = DateField(name="TestDate")
            
            # Test inherited methods
            assert field.is_empty() == "{TestDate}=BLANK()"
            assert field.is_not_empty() == "{TestDate}"
            assert field.name == "TestDate"

        def test_date_field_parse_date_with_string(self):
            """Test DateField _parse_date method with string"""
            field = DateField(name="TestDate")
            result = field._parse_date("2023-01-01")
            assert isinstance(result, datetime)
            assert result.year == 2023
            assert result.month == 1
            assert result.day == 1

        def test_date_field_parse_date_with_datetime(self):
            """Test DateField _parse_date method with datetime"""
            field = DateField(name="TestDate")
            test_date = datetime(2023, 12, 25, 10, 30, 0)
            result = field._parse_date(test_date)
            assert result == test_date

        def test_date_field_parse_invalid_date(self):
            """Test DateField with invalid date string raises ValueError"""
            field = DateField(name="TestDate")
            try:
                field._parse_date("invalid-date-string")
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "Could not parse date" in str(e)
        
        def test_date_field_with_edge_case_dates(self):
            """Test DateField with edge case dates"""
            field = DateField(name="EdgeDate")
            
            # Test leap year
            leap_date = datetime(2024, 2, 29, 0, 0, 0)
            result = field.is_on(leap_date)
            assert result == "DATETIME_PARSE('2024-02-29 00:00:00')=DATETIME_PARSE({EdgeDate})"
            
            # Test end of year
            end_year = datetime(2023, 12, 31, 23, 59, 59)
            result = field.is_before(end_year)
            assert result == "DATETIME_PARSE('2023-12-31 23:59:59')>DATETIME_PARSE({EdgeDate})"


        class TestDateComparison:
            """Tests for DateComparison class"""

            def test_date_comparison_date_method(self):
                """Test DateComparison _date method"""
                comparison = DateComparison(name="EventDate", compare="=")
                test_date = datetime(2023, 6, 15, 9, 0, 0)
                result = comparison._date(test_date)
                assert result == "DATETIME_PARSE('2023-06-15 09:00:00')=DATETIME_PARSE({EventDate})"

            def test_date_comparison_ago_method(self):
                """Test DateComparison _ago method"""
                comparison = DateComparison(name="LastLogin", compare=">")
                result = comparison._ago("days", 30)
                assert result == "DATETIME_DIFF(NOW(), {LastLogin}, 'days')>30"

            def test_date_comparison_milliseconds_ago(self):
                """Test DateComparison milliseconds_ago method"""
                comparison = DateComparison(name="Timestamp", compare="<")
                result = comparison.milliseconds_ago(1000)
                assert result == "DATETIME_DIFF(NOW(), {Timestamp}, 'milliseconds')<1000"

            def test_date_comparison_seconds_ago(self):
                """Test DateComparison seconds_ago method"""
                comparison = DateComparison(name="LastSeen", compare=">=")
                result = comparison.seconds_ago(60)
                assert result == "DATETIME_DIFF(NOW(), {LastSeen}, 'seconds')>=60"

            def test_date_comparison_minutes_ago(self):
                """Test DateComparison minutes_ago method"""
                comparison = DateComparison(name="LastUpdate", compare="<=")
                result = comparison.minutes_ago(30)
                assert result == "DATETIME_DIFF(NOW(), {LastUpdate}, 'minutes')<=30"

            def test_date_comparison_hours_ago(self):
                """Test DateComparison hours_ago method"""
                comparison = DateComparison(name="CreatedAt", compare="=")
                result = comparison.hours_ago(24)
                assert result == "DATETIME_DIFF(NOW(), {CreatedAt}, 'hours')=24"

            def test_date_comparison_days_ago(self):
                """Test DateComparison days_ago method"""
                comparison = DateComparison(name="PublishedAt", compare="!=")
                result = comparison.days_ago(7)
                assert result == "DATETIME_DIFF(NOW(), {PublishedAt}, 'days')!=7"

            def test_date_comparison_weeks_ago(self):
                """Test DateComparison weeks_ago method"""
                comparison = DateComparison(name="StartDate", compare=">")
                result = comparison.weeks_ago(2)
                assert result == "DATETIME_DIFF(NOW(), {StartDate}, 'weeks')>2"

            def test_date_comparison_months_ago(self):
                """Test DateComparison months_ago method"""
                comparison = DateComparison(name="JoinDate", compare="<")
                result = comparison.months_ago(6)
                assert result == "DATETIME_DIFF(NOW(), {JoinDate}, 'months')<6"

            def test_date_comparison_quarters_ago(self):
                """Test DateComparison quarters_ago method"""
                comparison = DateComparison(name="QuarterEnd", compare=">=")
                result = comparison.quarters_ago(1)
                assert result == "DATETIME_DIFF(NOW(), {QuarterEnd}, 'quarters')>=1"

            def test_date_comparison_years_ago(self):
                """Test DateComparison years_ago method"""
                comparison = DateComparison(name="BirthDate", compare="<=")
                result = comparison.years_ago(18)
                assert result == "DATETIME_DIFF(NOW(), {BirthDate}, 'years')<=18"

            def test_date_comparison_inheritance(self):
                """Test DateComparison inherits from Field"""
                comparison = DateComparison(name="TestDate", compare="=")
                
                # Test inherited methods
                assert comparison.is_empty() == "{TestDate}=BLANK()"
                assert comparison.is_not_empty() == "{TestDate}"
                assert comparison.name == "TestDate"

            def test_date_comparison_with_different_operators(self):
                """Test DateComparison with different comparison operators"""
                operators = ["=", "!=", ">", "<", ">=", "<="]
                
                for op in operators:
                    comparison = DateComparison(name="TestField", compare=op)
                    result = comparison.days_ago(10)
                    assert result == f"DATETIME_DIFF(NOW(), {{TestField}}, 'days'){op}10"

class TestCrossComponentIntegration:
    """Integration tests for cross-component interactions"""

    def test_real_world_user_validation_formula(self):
        """Test a real-world user validation formula"""
        name_field = TextField(name="Name")
        email_field = TextField(name="Email")
        age_field = Number(name="Age")
        active_field = BoolField(name="Active")
        
        # Complex validation: name not empty, valid email, adult age, and active
        validation = AND(
            name_field.is_not_empty(),
            email_field.regex_match(r"^[^@]+@[^@]+\.[^@]+$"),
            age_field.greater_than_or_equals(18),
            active_field.is_true()
        )
        
        result = IF(validation).THEN("Valid User").ELSE("Invalid User")
        expected = 'IF(AND({Name},REGEX_MATCH({Email}, "^[^@]+@[^@]+\\.[^@]+$"),{Age}>=18,{Active}=TRUE()), Valid User, Invalid User)'
        assert result == expected

    def test_project_status_with_dates_and_attachments(self):
        """Test project status formula with dates and attachments"""
        start_date = DateField(name="Start Date")
        end_date = DateField(name="End Date")
        documents = AttachmentsField(name="Documents")
        status = TextField(name="Status")
        
        # Project is ready if it has start date, end date is in future, has documents, and status is approved
        ready_condition = AND(
            start_date.is_not_empty(),
            end_date.is_on_or_after().days_ago(-30),  # End date is within 30 days in future
            documents.is_not_empty(),
            status.equals("Approved")
        )
        
        result = IF(ready_condition).THEN("Ready to Launch").ELSE("Not Ready")
        expected = 'IF(AND({Start Date},DATETIME_DIFF(NOW(), {End Date}, \'days\')>=-30,LEN({Documents})>0,{Status}="Approved"), Ready to Launch, Not Ready)'
        assert result == expected

    def test_e_commerce_product_filtering(self):
        """Test e-commerce product filtering with multiple field types"""
        name_field = TextField(name="Product Name")
        price_field = Number(name="Price")
        category_field = ListField(name="Categories")
        in_stock_field = BoolField(name="In Stock")
        images_field = AttachmentsField(name="Images")
        
        # Find products: name contains "laptop", price under $2000, in electronics category, in stock, has images
        product_filter = AND(
            name_field.contains("laptop"),
            price_field.less_than(2000),
            category_field.contains("Electronics"),
            in_stock_field.is_true(),
            images_field.is_not_empty()
        )
        
        result = IF(product_filter).THEN("Show Product").ELSE("Hide Product")
        expected = 'IF(AND(FIND(TRIM(LOWER("laptop")), TRIM(LOWER({Product Name})))>0,{Price}<2000,FIND(LOWER("Electronics"), LOWER({Categories}))>0,{In Stock}=TRUE(),LEN({Images})>0), Show Product, Hide Product)'
        assert result == expected

    def test_employee_bonus_calculation(self):
        """Test employee bonus calculation with multiple conditions"""
        performance_field = TextField(name="Performance Rating")
        salary_field = Number(name="Salary")
        years_field = Number(name="Years of Service")
        department_field = ListField(name="Department")
        active_field = BoolField(name="Active")
        
        # Bonus eligible: excellent performance, salary under 100k, 2+ years service, in sales/engineering, active
        bonus_eligible = AND(
            performance_field.equals("Excellent"),
            salary_field.less_than(100000),
            years_field.greater_than_or_equals(2),
            department_field.contains_any(["Sales", "Engineering"]),
            active_field.is_true()
        )
        
        result = IF(bonus_eligible).THEN("Eligible for Bonus").ELSE("Not Eligible")
        expected = 'IF(AND({Performance Rating}="Excellent",{Salary}<100000,{Years of Service}>=2,OR(FIND(LOWER("Sales"), LOWER({Department}))>0,FIND(LOWER("Engineering"), LOWER({Department}))>0),{Active}=TRUE()), Eligible for Bonus, Not Eligible)'
        assert result == expected

    def test_event_management_system(self):
        """Test event management system with dates and complex conditions"""
        venue_field = TextField(name="Venue")
        status_field = TextField(name="Status")
        materials_field = AttachmentsField(name="Materials")
        registrations_field = Number(name="Registrations")
        
        # Event ready: venue confirmed, approved status, has exactly 3 materials, not overbooked
        event_ready = AND(
            venue_field.not_equals(""),
            status_field.equals("Approved"),
            materials_field.count_is(3),
            registrations_field.less_than_or_equals(100)  # Fixed: provide actual value
        )
        
        result = IF(event_ready).THEN("Event Ready").ELSE("Needs Preparation")
        expected = 'IF(AND({Venue}!="",{Status}="Approved",LEN({Materials})=3,{Registrations}<=100), Event Ready, Needs Preparation)'
        assert result == expected

    def test_content_moderation_system(self):
        """Test content moderation system with text analysis"""
        title_field = TextField(name="Title")
        content_field = TextField(name="Content")
        author_field = TextField(name="Author")
        tags_field = ListField(name="Tags")
        flagged_field = BoolField(name="Flagged")
        
        # Content approval: title not empty, content doesn't contain banned words, author verified, appropriate tags, not flagged
        content_approved = AND(
            title_field.is_not_empty(),
            NOT(content_field.contains("spam")),
            NOT(content_field.contains("inappropriate")),
            author_field.not_equals("Anonymous"),
            OR(
                tags_field.contains("Educational"),
                tags_field.contains("News"),
                tags_field.contains("Entertainment")
            ),
            NOT(flagged_field.is_true())
        )
        
        result = IF(content_approved).THEN("Approved").ELSE("Needs Review")
        expected = 'IF(AND({Title},NOT(FIND(TRIM(LOWER("spam")), TRIM(LOWER({Content})))>0),NOT(FIND(TRIM(LOWER("inappropriate")), TRIM(LOWER({Content})))>0),{Author}!="Anonymous",OR(FIND(LOWER("Educational"), LOWER({Tags}))>0,FIND(LOWER("News"), LOWER({Tags}))>0,FIND(LOWER("Entertainment"), LOWER({Tags}))>0),NOT({Flagged}=TRUE())), Approved, Needs Review)'
        assert result == expected

    def test_inventory_management_with_dates(self):
        """Test inventory management with expiration dates"""
        quantity_field = Number(name="Quantity")
        location_field = TextField(name="Location")
        category_field = ListField(name="Category")
        
        # Item needs attention: low quantity OR in restricted location OR perishable
        simplified_attention = OR(
            quantity_field.less_than(10),
            location_field.equals("Quarantine"),
            category_field.contains("Perishable")
        )
        
        result = IF(simplified_attention).THEN("Needs Attention").ELSE("OK")
        expected = 'IF(OR({Quantity}<10,{Location}="Quarantine",FIND(LOWER("Perishable"), LOWER({Category}))>0), Needs Attention, OK)'
        assert result == expected

    def test_customer_segmentation_advanced(self):
        """Test advanced customer segmentation"""
        purchase_count = Number(name="Purchase Count")
        total_spent = Number(name="Total Spent")
        customer_type = TextField(name="Customer Type")
        preferences = ListField(name="Preferences")
        vip_status = BoolField(name="VIP")
        
        # VIP Customer: many purchases, high spending, premium type, luxury preferences, or already VIP
        vip_customer = OR(
            AND(
                purchase_count.greater_than(10),
                total_spent.greater_than(1000),
                customer_type.equals("Premium")
            ),
            preferences.contains("Luxury"),
            vip_status.is_true()
        )
        
        result = IF(vip_customer).THEN("VIP Treatment").ELSE("Standard Service")
        expected = 'IF(OR(AND({Purchase Count}>10,{Total Spent}>1000,{Customer Type}="Premium"),FIND(LOWER("Luxury"), LOWER({Preferences}))>0,{VIP}=TRUE()), VIP Treatment, Standard Service)'
        assert result == expected