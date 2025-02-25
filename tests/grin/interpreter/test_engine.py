import unittest
import io
import contextlib
from grin.interpreter.engine import InterpreterEngine
from grin.statements.basic_statements import LetStatement, PrintStatement
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
        var_token = GrinToken(GrinTokenKind.IDENTIFIER, "x")
        value_token = GrinToken(GrinTokenKind.LITERAL_INTEGER, 42)
        let_stmt = LetStatement(var_token, value_token)

        let_stmt.execute(self.engine)

        self.assertEqual(self.engine.variables["x"], 42)

    def test_print_statement(self):
        """Test PrintStatement prints the correct value"""
        value_token = GrinToken(GrinTokenKind.LITERAL_STRING, "Hello, Grin!")
        print_stmt = PrintStatement(value_token)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            print_stmt.execute(self.engine)

        self.assertEqual(output.getvalue().strip(), "Hello, Grin!")

    def test_label_indexing(self):
        """Test that labels are indexed correctly"""
        label1 = LabelStatement("start")
        label2 = LabelStatement("loop")
        program = [[label1], [label2]]

        engine = InterpreterEngine(program)

        self.assertEqual(engine.labels["start"], 0)
        self.assertEqual(engine.labels["loop"], 1)

    def test_duplicate_label_error(self):
        """Test that duplicate labels raise GrinRuntimeError"""
        label1 = LabelStatement("start")
        label2 = LabelStatement("start")  # Duplicate label
        program = [[label1], [label2]]

        with self.assertRaises(GrinRuntimeError):
            InterpreterEngine(program)

    def test_engine_run(self):
        """Test that the engine runs a simple program correctly"""
        var_token = GrinToken(GrinTokenKind.IDENTIFIER, "y")
        value_token = GrinToken(GrinTokenKind.LITERAL_INTEGER, 99)
        let_stmt = LetStatement(var_token, value_token)
        print_stmt = PrintStatement(var_token)
        program = [[let_stmt], [print_stmt]]

        engine = InterpreterEngine(program)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            engine.run()

        self.assertEqual(output.getvalue().strip(), "99")

    def test_ignore_label_execution(self):
        """Test that labels do not affect execution"""
        label = LabelStatement("here")
        var_token = GrinToken(GrinTokenKind.IDENTIFIER, "a")
        value_token = GrinToken(GrinTokenKind.LITERAL_INTEGER, 10)
        let_stmt = LetStatement(var_token, value_token)
        program = [[label], [let_stmt]]

        engine = InterpreterEngine(program)
        engine.run()

        self.assertEqual(engine.variables["a"], 10)


if __name__ == "__main__":
    unittest.main()
