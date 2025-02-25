from grin.statements.jump_statements import LabelStatement
from grin.interpreter.errors import GrinRuntimeError

class InterpreterEngine:
    def __init__(self, program):
        self.program = program
        self.current_line = 0
        self.variables = {}
        self.labels = {}
        self.terminate = False
        self.call_stack = []
        self._index_labels()

    def _index_labels(self) -> None:
        """Scan the program and record labels with their statement index."""
        for i, statement in enumerate(self.program):
            if isinstance(statement, list):
                if isinstance(statement[0], LabelStatement):
                    key_list = list(self.labels.keys())
                    if statement[0].label in key_list:
                        raise GrinRuntimeError("Cannot create two of the same label")

                    self.labels[statement[0].label] = i

    def run(self) -> None:
        """Runs the interpreter"""
        while self.current_line < len(self.program) and not self.terminate:
            statement = self.program[self.current_line]
            if isinstance(statement, list):
                if isinstance(statement[0], LabelStatement):
                    statement = statement[1]

            statement.execute(self)
            self.current_line += 1

__all__ = [
    InterpreterEngine.__name__
]