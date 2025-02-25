import unittest, io, sys, contextlib
from grin.statements.input_statements import InnumStatement, InstrStatement
from grin.token import GrinToken, GrinTokenKind
from grin.interpreter.errors import GrinRuntimeError



class MockInterpreterEngine:
    """Mock interpreter engine to test variable storage."""
    def __init__(self):
        self.variables = {}


class TestInnumStatement(unittest.TestCase):
    def setUp(self):
        """Set up a mock interpreter engine for testing."""
        self.engine = MockInterpreterEngine()

    def test_innum_statement_valid_integer(self):
        """Test InnumStatement with valid integer input."""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="num", location=None)
        stmt = InnumStatement(var_token)

        inp = io.StringIO("42\n")  # Simulating user input
        sys.stdin = inp
        out = io.StringIO()

        with contextlib.redirect_stdout(out):
            stmt.execute(self.engine)

        self.assertEqual(self.engine.variables["num"], 42)

    def test_innum_statement_valid_float(self):
        """Test InnumStatement with valid float input."""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="num", location=None)
        stmt = InnumStatement(var_token)

        inp = io.StringIO("3.14\n")  # Simulating user input
        sys.stdin = inp
        out = io.StringIO()

        with contextlib.redirect_stdout(out):
            stmt.execute(self.engine)

        self.assertEqual(self.engine.variables["num"], 3.14)

    def test_innum_statement_invalid_float_format(self):
        """Test InnumStatement with an invalid float format (e.g., '.5' instead of '0.5')."""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="num", location=None)
        stmt = InnumStatement(var_token)

        inp = io.StringIO(".5\n")  # Simulating invalid input
        sys.stdin = inp
        out = io.StringIO()

        with contextlib.redirect_stdout(out):
            with self.assertRaises(GrinRuntimeError) as cm:
                stmt.execute(self.engine)

        self.assertIn("needs to have an integer literal before the decimal place", str(cm.exception))

    def test_innum_statement_invalid_input(self):
        """Test InnumStatement with non-numeric input, expecting a runtime error."""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="num", location=None)
        stmt = InnumStatement(var_token)

        inp = io.StringIO("hello\n")  # Simulating invalid input
        sys.stdin = inp
        out = io.StringIO()

        with contextlib.redirect_stdout(out):
            with self.assertRaises(GrinRuntimeError) as cm:
                stmt.execute(self.engine)

        self.assertIn("Invalid numeric input for num", str(cm.exception))


class TestInstrStatement(unittest.TestCase):
    def setUp(self):
        """Set up a mock interpreter engine for testing."""
        self.engine = MockInterpreterEngine()

    def test_instr_statement_valid_string(self):
        """Test InstrStatement with valid string input."""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="text", location=None)
        stmt = InstrStatement(var_token)

        inp = io.StringIO("hello world\n")  # Simulating user input
        sys.stdin = inp
        out = io.StringIO()

        with contextlib.redirect_stdout(out):
            stmt.execute(self.engine)

        self.assertEqual(self.engine.variables["text"], "hello world")

    def test_instr_statement_empty_string(self):
        """Test InstrStatement with empty input."""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="text", location=None)
        stmt = InstrStatement(var_token)

        inp = io.StringIO("\n")  # Simulating empty input
        sys.stdin = inp
        out = io.StringIO()

        with contextlib.redirect_stdout(out):
            stmt.execute(self.engine)

        self.assertEqual(self.engine.variables["text"], "")  # Should store an empty string


if __name__ == "__main__":
    unittest.main()