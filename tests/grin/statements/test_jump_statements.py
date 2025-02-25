from grin import compare, GrinToken, GrinTokenKind, GrinRuntimeError
import unittest

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