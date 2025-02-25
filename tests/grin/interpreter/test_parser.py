import unittest
from grin.interpreter.parser import statement_creator, parse_statements_into_objects
from grin.token import GrinToken, GrinTokenKind
from grin.statements.basic_statements import LetStatement, PrintStatement, EndStatement
from grin.statements.jump_statements import LabelStatement
from grin.interpreter.errors import GrinParseError


class TestParser(unittest.TestCase):
    def test_statement_creator_let(self):
        """Test statement_creator with a Let statement"""
        tokens = [
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=None),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="x", location=None),
            GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="42", location=None, value=42),
        ]

        statement = statement_creator(tokens)
        self.assertIsInstance(statement, LetStatement)
        self.assertEqual(statement.var.text(), "x")
        self.assertEqual(statement.value.value(), 42)

    def test_statement_creator_print(self):
        """Test statement_creator with a Print statement"""
        tokens = [
            GrinToken(kind=GrinTokenKind.PRINT, text="PRINT", location=None),
            GrinToken(kind=GrinTokenKind.LITERAL_STRING, text='"Hello"', location=None, value="Hello"),
        ]

        statement = statement_creator(tokens)
        self.assertIsInstance(statement, PrintStatement)
        self.assertEqual(statement.print_value.value(), "Hello")

    def test_statement_creator_label(self):
        """Test statement_creator with a label"""
        tokens = [
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="start", location=None),
            GrinToken(kind=GrinTokenKind.COLON, text=":", location=None),
        ]

        statement = statement_creator(tokens)
        self.assertIsInstance(statement, LabelStatement)
        self.assertEqual(statement.label, "start")

    def test_statement_creator_invalid(self):
        """Test statement_creator with an invalid statement"""
        tokens = [
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="INVALID", location=None),
        ]

        with self.assertRaises(GrinParseError) as cm:
            statement_creator(tokens)

        self.assertIn("Unknown statement", str(cm.exception))

    def test_parse_statements_single_let(self):
        """Test parse_statements_into_objects with a single Let statement"""
        tokens = [[
            GrinToken(kind=GrinTokenKind.LET, text="LET", location=None),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="y", location=None),
            GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="99", location=None, value=99),
        ]]

        statements = parse_statements_into_objects(tokens)
        self.assertIsInstance(statements[0], LetStatement)
        self.assertEqual(statements[0].var.text(), "y")
        self.assertEqual(statements[0].value.value(), 99)

    def test_parse_statements_single_print(self):
        """Test parse_statements_into_objects with a single Print statement"""
        tokens = [[
            GrinToken(kind=GrinTokenKind.PRINT, text="PRINT", location=None),
            GrinToken(kind=GrinTokenKind.LITERAL_STRING, text='"World"', location=None, value="World"),
        ]]

        statements = parse_statements_into_objects(tokens)
        self.assertIsInstance(statements[0], PrintStatement)
        self.assertEqual(statements[0].print_value.value(), "World")

    def test_parse_statements_with_label(self):
        """Test parse_statements_into_objects with a labeled statement"""
        tokens = [[
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="loop", location=None),
            GrinToken(kind=GrinTokenKind.COLON, text=":", location=None),
            GrinToken(kind=GrinTokenKind.PRINT, text="PRINT", location=None),
            GrinToken(kind=GrinTokenKind.LITERAL_STRING, text='"Looping"', location=None, value="Looping"),
        ]]

        statements = parse_statements_into_objects(tokens)
        self.assertIsInstance(statements[0], list)
        self.assertIsInstance(statements[0][0], LabelStatement)
        self.assertIsInstance(statements[0][1], PrintStatement)
        self.assertEqual(statements[0][0].label, "loop")
        self.assertEqual(statements[0][1].print_value.value(), "Looping")



    def test_parse_statements_invalid_statement(self):
        """Test parse_statements_into_objects with an invalid statement"""
        tokens = [[
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="UNKNOWN", location=None),
        ]]

        with self.assertRaises(GrinParseError):
            parse_statements_into_objects(tokens)

    def test_parse_statements_label_with_invalid_statement(self):
        """Test parse_statements_into_objects with a label followed by an invalid statement"""
        tokens = [[
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="loop", location=None),
            GrinToken(kind=GrinTokenKind.COLON, text=":", location=None),
            GrinToken(kind=GrinTokenKind.IDENTIFIER, text="INVALID", location=None),
        ]]

        with self.assertRaises(GrinParseError) as cm:
            parse_statements_into_objects(tokens)

        self.assertIn("Error after label loop", str(cm.exception))

    def test_statement_creator_let(self):
        """Test statement_creator with a Let statement"""
        tokens = [
            GrinToken(kind = GrinTokenKind.LET, text = "LET", location = None),
            GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "x", location = None),
            GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "42", location = None,
                      value = 42),
        ]

        statement = statement_creator(tokens)
        self.assertIsInstance(statement, LetStatement)
        self.assertEqual(statement.var.text(), "x")
        self.assertEqual(statement.value.value(), 42)

    def test_statement_creator_print(self):
        """Test statement_creator with a Print statement"""
        tokens = [
            GrinToken(kind = GrinTokenKind.PRINT, text = "PRINT", location = None),
            GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = '"Hello"', location = None,
                      value = "Hello"),
        ]

        statement = statement_creator(tokens)
        self.assertIsInstance(statement, PrintStatement)
        self.assertEqual(statement.print_value.value(), "Hello")

    def test_statement_creator_end(self):
        """Test statement_creator with an End statement"""
        tokens = [
            GrinToken(kind = GrinTokenKind.END, text = "END", location = None),
        ]

        statement = statement_creator(tokens)
        self.assertIsInstance(statement, EndStatement)

    def test_statement_creator_label(self):
        """Test statement_creator with a label"""
        tokens = [
            GrinToken(kind = GrinTokenKind.IDENTIFIER, text = "start", location = None),
            GrinToken(kind = GrinTokenKind.COLON, text = ":", location = None),
        ]

        statement = statement_creator(tokens)
        self.assertIsInstance(statement, LabelStatement)
        self.assertEqual(statement.label, "start")


    def test_statement_creator_empty(self):
        """Test statement_creator with an empty token list"""
        tokens = []

        with self.assertRaises(GrinParseError) as cm:
            statement_creator(tokens)

        self.assertIn("Empty statement", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
