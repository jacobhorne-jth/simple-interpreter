from grin.statements.basic_statements import Statement
from grin.interpreter.errors import GrinRuntimeError
from grin.statements.basic_statements import evaluate_expression


class MathStatement(Statement):
    """Base class for math operations like ADD, SUB, MULT, DIV"""
    def __init__(self, var, value):
        self.var = var
        self.value = value

    def operate(self, left, right):
        raise NotImplementedError

    def execute(self, interpreter_engine):
        if self.var.text() not in interpreter_engine.variables:
            interpreter_engine.variables[self.var.text()] = 0
        left = evaluate_expression(self.var, interpreter_engine)
        right = evaluate_expression(self.value, interpreter_engine)
        interpreter_engine.variables[self.var.text()] = self.operate(left, right)

class AddStatement(MathStatement):
    """Add statement class for Grin Add statements"""
    def operate(self, left, right):
        if isinstance(left, str) and isinstance(right, str):
            return left + right
        elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        raise GrinRuntimeError(f'Cannot add {type(right).__name__} to {type(left).__name__}')

class SubStatement(MathStatement):
    """Sub statement class for Grin Sub statements"""
    def operate(self, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right
        raise GrinRuntimeError(f'Cannot subtract {type(right).__name__} from {type(left).__name__}')

class MultStatement(MathStatement):
    """Mult statement class for Grin Mult statements"""
    def operate(self, left, right):
        if isinstance(left, str) and isinstance(right, int):
            if right >= 0:
                return left * right
            else:
                raise GrinRuntimeError(f'Cannot multiply a string with a negative integer')

        elif isinstance(left, int) and isinstance(right, str):
            if left >= 0:
                return right * left
            else:
                raise GrinRuntimeError(f'Cannot multiply a string with a negative integer')
        elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        raise GrinRuntimeError(f'Cannot multiply {type(left).__name__} with {type(right).__name__}')

class DivStatement(MathStatement):
    """Div statement class for Grin Div statements"""
    def operate(self, left, right):
        if right == 0:
            raise GrinRuntimeError('Cannot divide by 0')
        if isinstance(left, int) and isinstance(right, int):
            return int(left / right)
        elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left / right
        raise GrinRuntimeError(f'Cannot divide {type(left).__name__} by {type(right).__name__}')


__all__ = [
    MathStatement.__name__,
    AddStatement.__name__,
    SubStatement.__name__,
    MultStatement.__name__,
    DivStatement.__name__
]