import unittest
import io
import contextlib
from grin.interpreter.engine import InterpreterEngine
from grin.statements.basic_statements import LetStatement, PrintStatement, EndStatement
from grin.statements.jump_statements import LabelStatement
from grin.token import GrinToken, GrinTokenKind
from grin.interpreter.errors import GrinRuntimeError


class TestInterpreterEngine(unittest.TestCase):
    def setUp(self):
        """Set up an instance of InterpreterEngine for testing"""
        self.program = []
        self.engine = InterpreterEngine(self.program)

    def test_let_statement(self):
        """Test LetStatement assigns values correctly"""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="x", location=None)
        value_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="42", location=None, value=42)
        let_stmt = LetStatement(var_token, value_token)

        let_stmt.execute(self.engine)

        self.assertEqual(self.engine.variables["x"], 42)

    def test_print_statement(self):
        """Test PrintStatement prints the correct value"""
        value_token = GrinToken(kind=GrinTokenKind.LITERAL_STRING, text='"Hello, Grin!"', location=None, value="Hello, Grin!")
        print_stmt = PrintStatement(value_token)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            print_stmt.execute(self.engine)

        self.assertEqual(output.getvalue().strip(), "Hello, Grin!")

    def test_label_indexing(self):
        """Test that labels are indexed correctly"""
        label1 = LabelStatement("start")
        statement1 = PrintStatement(1)
        label2 = LabelStatement("loop")  # Duplicate label
        statement2 = PrintStatement(1)
        program = [[label1, statement1], [label2, statement2]]

        engine = InterpreterEngine(program)

        self.assertEqual(engine.labels["start"], 0)
        self.assertEqual(engine.labels["loop"], 1)

    def test_duplicate_label_error(self):
        """Test that duplicate labels raise GrinRuntimeError"""
        label1 = LabelStatement("start")
        statement1 = PrintStatement(1)
        label2 = LabelStatement("start")  # Duplicate label
        statement2 = PrintStatement(1)
        program = [[label1, statement1], [label2, statement2]]  # Labels should be in a flat list

        with self.assertRaises(GrinRuntimeError):
            InterpreterEngine(program)

    def test_engine_run(self):
        """Test that the engine runs a simple program correctly"""
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="y", location=None)
        value_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="99", location=None, value=99)
        let_stmt = LetStatement(var_token, value_token)
        print_stmt = PrintStatement(var_token)
        program = [let_stmt, print_stmt]  # Statements should not be nested in lists

        engine = InterpreterEngine(program)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            engine.run()

        self.assertEqual(output.getvalue().strip(), "99")

    def test_ignore_label_execution(self):
        """Test that labels do not affect execution"""
        label = LabelStatement("here")
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="a", location=None)
        value_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="10", location=None, value=10)
        let_stmt = LetStatement(var_token, value_token)
        program = [label, let_stmt]  # Ensure statements are correctly structured

        engine = InterpreterEngine(program)
        engine.run()

        self.assertEqual(engine.variables["a"], 10)

    def test_end_statement_terminates_execution(self):
        """Test that EndStatement correctly terminates execution"""
        end_stmt = EndStatement()
        var_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="b", location=None)
        value_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="20", location=None, value=20)
        let_stmt = LetStatement(var_token, value_token)
        program = [let_stmt, end_stmt, PrintStatement(value_token)]  # Ensure execution stops before printing

        engine = InterpreterEngine(program)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            engine.run()

        self.assertTrue(engine.terminate)  # Should be set to True
        self.assertNotIn("20", output.getvalue())  # "20" should not be printed because EndStatement stops execution


if __name__ == "__main__":
    unittest.main()
