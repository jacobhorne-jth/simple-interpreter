from grin.token import GrinTokenKind, GrinToken
from grin.interpreter.errors import GrinRuntimeError

def evaluate_expression(value, engine):
    """Evaluates whether a value is a literal, variable, or label reference."""
    if isinstance(value, GrinToken):
        if value.kind() in (
        GrinTokenKind.LITERAL_FLOAT, GrinTokenKind.LITERAL_INTEGER, GrinTokenKind.LITERAL_STRING):
            return value.value()
        elif value.kind() == GrinTokenKind.IDENTIFIER:
            return engine.variables.get(value.text(), 0)
    elif isinstance(value, str):
        return value
    elif isinstance(value, int):
        return value
    raise GrinRuntimeError(f"Invalid value: {value}")

class Statement:
    """Base class for all Grin statements"""
    def execute(self, interpreter_engine):
        raise NotImplementedError("Subclasses must implement execute()")

class LetStatement(Statement):
    """Let statement class for Grin Let statements"""
    def __init__(self, var, value):
        self.var = var
        self.value = value

    def execute(self, interpreter_engine):
        interpreter_engine.variables[self.var.text()] = evaluate_expression(self.value,
                                                                            interpreter_engine)
class PrintStatement(Statement):
    """Print statement class for Grin Print statements"""
    def __init__(self, value):
        self.print_value = value

    def execute(self, interpreter_engine):
        print(evaluate_expression(self.print_value, interpreter_engine))

class EndStatement(Statement):
    """End statement class for Grin End statements"""
    def execute(self, interpreter_engine):
        interpreter_engine.terminate = True


__all__ = [
    evaluate_expression.__name__,
    Statement.__name__,
    LetStatement.__name__,
    PrintStatement.__name__,
    EndStatement.__name__
]