import unittest
from grin.interpreter.errors import GrinRuntimeError
from grin.token import GrinTokenKind, GrinToken
from grin.statements.jump_statements import GotoStatement, GosubStatement, ReturnStatement, LabelStatement, compare

class MockInterpreterEngine:
    """Mock interpreter engine to test jump statements."""
    def __init__(self):
        self.variables = {}
        self.labels = {}
        self.call_stack = []
        self.current_line = 0
        self.program = [None] * 10  # Simulate a program with 10 lines

class TestGotoStatement(unittest.TestCase):
    def setUp(self):
        self.engine = MockInterpreterEngine()

    def test_goto_valid_label_jump(self):
        """Test GotoStatement successfully jumps to a label"""
        self.engine.labels["start"] = 5
        target_token = GrinToken(kind=GrinTokenKind.LITERAL_STRING, text="start", location=None, value = "start")
        stmt = GotoStatement(target_token)

        self.engine.current_line = 1  # Ensure current line is not 0
        stmt.execute(self.engine)

        self.assertEqual(self.engine.current_line, 4)

    def test_goto_valid_relative_jump(self):
        """Test GotoStatement successfully jumps a relative number of lines"""
        target_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="3", location=None, value=3)
        stmt = GotoStatement(target_token)

        self.engine.current_line = 1
        stmt.execute(self.engine)

        self.assertEqual(self.engine.current_line, 3)

    def test_goto_label_not_found(self):
        """Test GotoStatement raises an error when label is not found"""
        target_token = GrinToken(kind=GrinTokenKind.LITERAL_STRING, text="missing", location=None, value = "missing")

        stmt = GotoStatement(target_token)

        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn('Label "missing" not found.', str(cm.exception))

    def test_goto_jump_out_of_bounds(self):
        """Test GotoStatement raises an error when jumping out of program bounds"""
        target_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="10", location=None, value=10)
        stmt = GotoStatement(target_token)

        self.engine.current_line = 2
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("jumps out of bounds", str(cm.exception))

    def test_goto_invalid_target_type(self):
        """Test GotoStatement raises an error for an invalid target type"""
        target_token = GrinToken(kind=GrinTokenKind.LITERAL_FLOAT, text="3.5", location=None, value=3.5)
        stmt = GotoStatement(target_token)

        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Invalid target type for GOTO", str(cm.exception))

    def test_goto_zero_jump_error(self):
        """Test GotoStatement raises an error when attempting to jump 0 lines"""
        target_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="0", location=None, value=0)
        stmt = GotoStatement(target_token)

        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("Cannot jump 0 lines", str(cm.exception))


class TestGosubStatement(unittest.TestCase):
    def setUp(self):
        self.engine = MockInterpreterEngine()

    def test_gosub_saves_return_address(self):
        """Test GosubStatement saves return address and jumps correctly"""
        self.engine.labels["subroutine"] = 3
        target_token = GrinToken(kind=GrinTokenKind.IDENTIFIER, text="subroutine", location=None)
        stmt = GosubStatement(target_token)

        self.engine.current_line = 1
        stmt.execute(self.engine)

        self.assertEqual(self.engine.call_stack[-1], 1)  # Return point saved
        self.assertEqual(self.engine.current_line, 0)  # Adjusted for execution

    def test_gosub_jump_out_of_bounds(self):
        """Test GosubStatement raises an error when jumping out of program bounds"""
        target_token = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="10", location=None, value=10)
        stmt = GosubStatement(target_token)

        self.engine.current_line = 2
        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("jumps out of bounds", str(cm.exception))


class TestReturnStatement(unittest.TestCase):
    def setUp(self):
        self.engine = MockInterpreterEngine()

    def test_return_pops_call_stack(self):
        """Test ReturnStatement restores previous line from call stack"""
        self.engine.call_stack.append(2)
        stmt = ReturnStatement()

        stmt.execute(self.engine)

        self.assertEqual(self.engine.current_line, 2)

    def test_return_without_gosub(self):
        """Test ReturnStatement raises an error when there is no matching GOSUB"""
        stmt = ReturnStatement()

        with self.assertRaises(GrinRuntimeError) as cm:
            stmt.execute(self.engine)

        self.assertIn("RETURN statement encountered without a matching GOSUB.", str(cm.exception))


class TestLabelStatement(unittest.TestCase):
    def test_label_statement_execution(self):
        """Test LabelStatement execution does nothing (as expected)"""
        label = LabelStatement("start")

        engine = MockInterpreterEngine()
        label.execute(engine)

        self.assertEqual(engine.current_line, 0)  # No changes should occur


class TestCompareFunction(unittest.TestCase):

    def test_compare_equal(self):
        """Test compare function for equality check"""
        left = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        right = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        operator = GrinToken(kind=GrinTokenKind.EQUAL, text="==", location=None)

        self.assertTrue(compare(left, operator, right))

    def test_compare_not_equal(self):
        """Test compare function for inequality check"""
        left = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        right = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="10", location=None, value=10)
        operator = GrinToken(kind=GrinTokenKind.NOT_EQUAL, text="!=", location=None)

        self.assertTrue(compare(left, operator, right))

    def test_compare_less_than(self):
        """Test compare function for '<' operator."""
        left = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="3", location=None, value=3)
        right = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        operator = GrinToken(kind=GrinTokenKind.LESS_THAN, text="<", location=None)

        self.assertTrue(compare(left, operator, right))  # 3 < 5 should be True

    def test_compare_less_than_or_equal(self):
        """Test compare function for '<=' operator."""
        left = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        right = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        operator = GrinToken(kind=GrinTokenKind.LESS_THAN_OR_EQUAL, text="<=", location=None)

        self.assertTrue(compare(left, operator, right))  # 5 <= 5 should be True

    def test_compare_greater_than(self):
        """Test compare function for '>' operator."""
        left = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="10", location=None, value=10)
        right = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        operator = GrinToken(kind=GrinTokenKind.GREATER_THAN, text=">", location=None)

        self.assertTrue(compare(left, operator, right))  # 10 > 5 should be True

    def test_compare_greater_than_or_equal(self):
        """Test compare function for '>=' operator."""
        left = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="8", location=None, value=8)
        right = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="8", location=None, value=8)
        operator = GrinToken(kind=GrinTokenKind.GREATER_THAN_OR_EQUAL, text=">=", location=None)

        self.assertTrue(compare(left, operator, right))  # 8 >= 8 should be True

    def test_compare_invalid_operator(self):
        """Test compare function raises an error for an invalid operator."""
        left = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        right = GrinToken(kind=GrinTokenKind.LITERAL_INTEGER, text="5", location=None, value=5)
        invalid_operator = GrinToken(kind=GrinTokenKind.DOT, text=".", location=None)

        with self.assertRaises(GrinRuntimeError) as cm:
            compare(left, invalid_operator, right)

        self.assertIn("Invalid comparison operator", str(cm.exception))

    def test_compare_integer_and_float(self):
        """Test compare function where int is converted to float and compared."""
        left = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "5", location = None,
                         value = 5)
        right = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = "5.5", location = None,
                          value = 5.5)
        operator = GrinToken(kind = GrinTokenKind.LESS_THAN, text = "<", location = None)

        self.assertTrue(compare(left, operator, right))

        left_float = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = "5.5", location = None,
                               value = 5.5)
        right_int = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = "5", location = None,
                              value = 5)
        operator_gt = GrinToken(kind = GrinTokenKind.GREATER_THAN, text = ">", location = None)

        self.assertTrue(compare(left_float, operator_gt, right_int))


if __name__ == "__main__":
    unittest.main()