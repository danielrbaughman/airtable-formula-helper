from airtableformulahelpers import AND, NOT, OR, XOR, BoolField, TextField


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


class TestLogicalFunctionIntegration:
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


class TestLogicalFunctionEdgeCases:
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