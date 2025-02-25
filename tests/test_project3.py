import unittest, io, sys, contextlib
from project3 import main


class TestProject3(unittest.TestCase):
    def setUp(self):
        """Redirect stdin and stdout for testing."""
        self.input_backup = sys.stdin
        self.output_backup = sys.stdout
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Restore stdin and stdout after each test."""
        sys.stdin = self.input_backup
        sys.stdout = self.output_backup

    def test_main_valid_program(self):
        """Test main() with a valid sequence of Grin statements."""
        user_input = io.StringIO("LET A 5\nPRINT A\n.")
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertIn("5", output)

    def test_main_invalid_syntax(self):
        """Test main() handling of an invalid statement."""
        user_input = io.StringIO("INVALID A B C\n.")
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertIn("Error during parsing: Line 1 Column 9: GrinTokenKind.COLON", output)

    def test_main_runtime_error(self):
        """Test main() handling of a runtime error (e.g., invalid math operation)."""
        user_input = io.StringIO("LET A 5\nDIV A 0\n.")
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertIn("Cannot divide by 0", output)

    def test_main_empty_input(self):
        """Test main() with no input."""
        user_input = io.StringIO(".\n")
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "")  # No output expected

    def test_main_multiple_statements(self):
        """Test main() with multiple valid statements."""
        user_input = io.StringIO("LET A 10\nLET B 20\nADD A B\nPRINT A\n.")
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertIn("30", output)

    def test_main_label_and_goto(self):
        """Test main() with labels and GOTO statement."""
        user_input = io.StringIO('START: LET A 1\nGOTO "ENDLABEL"\nPRINT A\nENDLABEL: PRINT 2\n .')
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertNotIn("1", output)  # Should not print A since GOTO skips it
        self.assertIn("2", output)

    def test_main_goto_invalid_label(self):
        """Test main() with a GOTO to a nonexistent label."""
        user_input = io.StringIO('GOTO "MISSINGLABEL"\n.')
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertIn('Label "MISSINGLABEL" not found.', output)

    def test_main_end_statement(self):
        """Test main() with an END statement terminating execution."""
        user_input = io.StringIO("LET X 5\nEND\nPRINT X\n.")
        sys.stdin = user_input

        with contextlib.redirect_stdout(self.captured_output):
            main()

        output = self.captured_output.getvalue().strip()
        self.assertNotIn("5", output)  # Should not print X because END stops execution


if __name__ == "__main__":
    unittest.main()