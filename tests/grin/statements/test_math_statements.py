import unittest
from grin.statements.math_statements import AddStatement, SubStatement, MultStatement, DivStatement
from grin.token import GrinToken, GrinTokenKind
from grin.interpreter.errors import GrinRuntimeError


class MockInterpreterEngine:
    """Mock interpreter engine to test variable storage."""
    def __init__(self):
        self.variables = {}


class TestMathStatements(unittest.TestCase):
    def setUp(self):
        """Set up a mock interpreter engine for testing."""
        self.engine = MockInterpreterEngine()

    ## ADD TESTS ##
    def test_add_valid_numbers(self):
        """Test AddStatement with valid integer addition."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "x", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "5", location = None,
                                value = 5)
        stmt = AddStatement(var_token, value_token)

        self.engine.variables["x"] = 10
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["x"], 15)

    def test_add_valid_strings(self):
        """Test AddStatement with string concatenation."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "s", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = '"world"',
                                location = None, value = "world")
        stmt = AddStatement(var_token, value_token)

        self.engine.variables["s"] = "hello "
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["s"], "hello world")

    def test_add_invalid_int_str(self):
        """Test AddStatement with int + str (should raise error)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "x", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = '"hello"',
                                location = None, value = "hello")
        stmt = AddStatement(var_token, value_token)

        self.engine.variables["x"] = 10
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Cannot add str to int", str(cm.exception))

    ## SUB TESTS ##
    def test_sub_valid_numbers(self):
        """Test SubStatement with valid integer subtraction."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "y", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "3", location = None,
                                value = 3)
        stmt = SubStatement(var_token, value_token)

        self.engine.variables["y"] = 10
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["y"], 7)

    def test_sub_invalid_str_int(self):
        """Test SubStatement with str - int (should raise error)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "a", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "5", location = None,
                                value = 5)
        stmt = SubStatement(var_token, value_token)

        self.engine.variables["a"] = "hello"
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Cannot subtract int from str", str(cm.exception))

    ## MULT TESTS ##
    def test_mult_valid_numbers(self):
        """Test MultStatement with valid integer multiplication."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "z", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "4", location = None,
                                value = 4)
        stmt = MultStatement(var_token, value_token)

        self.engine.variables["z"] = 2
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["z"], 8)

    def test_mult_valid_string_int(self):
        """Test MultStatement with string * int (valid case)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "s", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "3", location = None,
                                value = 3)
        stmt = MultStatement(var_token, value_token)

        self.engine.variables["s"] = "ha"
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["s"], "hahaha")

    def test_mult_valid_string_int_again(self):
        """Test MultStatement with string * int (valid case)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "s", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = "ha", location = None,
                                value = 'ha')
        stmt = MultStatement(var_token, value_token)

        self.engine.variables["s"] = 3
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["s"], "hahaha")

    def test_mult_str_negative_int(self):
        """Test MultStatement with str and negative int"""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "s", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = "ha", location = None,
                                value = 'ha')
        stmt = MultStatement(var_token, value_token)

        self.engine.variables["s"] = -3
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

    def test_mult_str_negative_int_again(self):
        """Test MultStatement with str and negative int"""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "s", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = "-3", location = None,
                                value = -3)
        stmt = MultStatement(var_token, value_token)

        self.engine.variables["s"] = 'ha'
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

    def test_math_statement_variable_not_exist(self):
        """Test when a variable does not exist, it is initialized to 0 before operation."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "m", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "5", location = None,
                                value = 5)
        stmt = AddStatement(var_token, value_token)

        # The variable "m" does not exist in interpreter storage
        stmt.execute(self.engine)

        # It should be initialized to 0, then add 5
        self.assertEqual(self.engine.variables["m"], 5)

    def test_mult_invalid_str_str(self):
        """Test MultStatement with str * str (should raise error)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "s", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = '"abc"',
                                location = None, value = "abc")
        stmt = MultStatement(var_token, value_token)

        self.engine.variables["s"] = "hello"
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Cannot multiply str with str", str(cm.exception))

    ## DIV TESTS ##
    def test_div_valid_numbers(self):
        """Test DivStatement with valid integer division."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "n", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "2", location = None,
                                value = 2)
        stmt = DivStatement(var_token, value_token)

        self.engine.variables["n"] = 8
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["n"], 4)

    def test_div_by_zero(self):
        """Test DivStatement for division by zero (should raise error)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "n", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "0", location = None,
                                value = 0)
        stmt = DivStatement(var_token, value_token)

        self.engine.variables["n"] = 10
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Cannot divide by 0", str(cm.exception))

    def test_div_invalid_str_int(self):
        """Test DivStatement with str / int (should raise error)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "x", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "2", location = None,
                                value = 2)
        stmt = DivStatement(var_token, value_token)

        self.engine.variables["x"] = "hello"
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Cannot divide str by int", str(cm.exception))

    def test_div_invalid_float_str(self):
        """Test DivStatement with float / str (should raise error)."""
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "y", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = '"test"',
                                location = None, value = "test")
        stmt = DivStatement(var_token, value_token)

        self.engine.variables["y"] = 5.5
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Cannot divide float by str", str(cm.exception))


if __name__ == "__main__":
    unittest.main()