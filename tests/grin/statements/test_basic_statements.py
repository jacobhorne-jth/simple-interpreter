import unittest
import io
import contextlib
from grin.interpreter.errors import GrinRuntimeError
from grin.token import GrinToken, GrinTokenKind
from grin.statements.basic_statements import evaluate_expression, LetStatement, PrintStatement


class MockInterpreterEngine:
    """Mock interpreter engine to test variable storage."""

    def __init__(self):
        self.variables = {}


class TestEvaluateExpression(unittest.TestCase):
    def setUp(self):
        self.engine = MockInterpreterEngine()

    def test_evaluate_literal_integer(self):
        token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "42", location = None,
                          value = 42)
        self.assertEqual(evaluate_expression(token, self.engine), 42)

    def test_evaluate_literal_float(self):
        token = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = "3.14", location = None,
                          value = 3.14)
        self.assertEqual(evaluate_expression(token, self.engine), 3.14)

    def test_evaluate_literal_string(self):
        token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = "hello", location = None,
                          value = "hello")
        self.assertEqual(evaluate_expression(token, self.engine), "hello")

    def test_evaluate_identifier_existing_variable(self):
        self.engine.variables["x"] = 10
        token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "x", location = None)
        self.assertEqual(evaluate_expression(token, self.engine), 10)

    def test_evaluate_identifier_nonexistent_variable(self):
        token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "y", location = None)
        self.assertEqual(evaluate_expression(token, self.engine), 0)

    def test_evaluate_raw_string(self):
        self.assertEqual(evaluate_expression("test", self.engine), "test")

    def test_evaluate_raw_integer(self):
        self.assertEqual(evaluate_expression(99, self.engine), 99)

    def test_evaluate_invalid_value(self):
        with self.assertRaises(GrinRuntimeError):
            evaluate_expression([], self.engine)


class TestLetStatement(unittest.TestCase):
    def setUp(self):
        self.engine = MockInterpreterEngine()

    def test_let_statement_assigns_value(self):
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "x", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "5", location = None,
                                value = 5)
        stmt = LetStatement(var_token, value_token)
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["x"], 5)

    def test_let_statement_overwrites_existing_variable(self):
        self.engine.variables["x"] = 10
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "x", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "20", location = None,
                                value = 20)
        stmt = LetStatement(var_token, value_token)
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["x"], 20)

    def test_let_statement_assigns_string(self):
        var_token = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "y", location = None)
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = "hello",
                                location = None, value = "hello")
        stmt = LetStatement(var_token, value_token)
        stmt.execute(self.engine)
        self.assertEqual(self.engine.variables["y"], "hello")


class TestPrintStatement(unittest.TestCase):
    def setUp(self):
        self.engine = MockInterpreterEngine()

    def test_print_statement_outputs_value(self):
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = "Hello",
                                location = None, value = "Hello")
        stmt = PrintStatement(value_token)

        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            stmt.execute(self.engine)

        self.assertEqual(captured_output.getvalue().strip(), "Hello")

    def test_print_statement_outputs_integer(self):
        value_token = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "42", location = None,
                                value = 42)
        stmt = PrintStatement(value_token)

        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            stmt.execute(self.engine)

        self.assertEqual(captured_output.getvalue().strip(), "42")


if __name__ == "__main__":
    unittest.main()
