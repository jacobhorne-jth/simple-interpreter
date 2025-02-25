from grin.statements.basic_statements import Statement
from grin.interpreter.errors import GrinRuntimeError
from grin.token import GrinTokenKind
from grin.statements.basic_statements import evaluate_expression


def compare(left, operator, right):
    """Evaluates a comparison between left and right values using the given operator."""
    left_value = left if isinstance(left, (int, float, str)) else left.value()
    right_value = right if isinstance(right, (int, float, str)) else right.value()

    if isinstance(left_value, int) and isinstance(right_value, float):
        left_value = float(left_value)
    elif isinstance(left_value, float) and isinstance(right_value, int):
        right_value = float(right_value)
    elif type(left_value) != type(right_value):
        raise GrinRuntimeError(f"Cannot compare different types: {type(left_value).__name__} and {type(right_value).__name__}")

    if operator.kind() == GrinTokenKind.EQUAL:
        return left_value == right_value
    elif operator.kind() == GrinTokenKind.NOT_EQUAL:
        return left_value != right_value
    elif operator.kind() == GrinTokenKind.LESS_THAN:
        return left_value < right_value
    elif operator.kind() == GrinTokenKind.LESS_THAN_OR_EQUAL:
        return left_value <= right_value
    elif operator.kind() == GrinTokenKind.GREATER_THAN:
        return left_value > right_value
    elif operator.kind() == GrinTokenKind.GREATER_THAN_OR_EQUAL:
        return left_value >= right_value
    else:
        raise GrinRuntimeError(f"Invalid comparison operator: {operator.text()}")


class JumpStatement(Statement):
    """Base class for all Grin Jump statements"""
    def __init__(self, target, condition_left = None, operator = None, condition_right = None):
        self.target = target
        self.condition_left = condition_left
        self.operator = operator
        self.condition_right = condition_right

    def jump_to(self, interpreter_engine):
        """Moves execution to a new statement index, ensuring correct jumps."""
        target_value = evaluate_expression(self.target, interpreter_engine)

        if isinstance(target_value, int):  # Relative jump by line number
            new_line = interpreter_engine.current_line + target_value
            if new_line < 0 or new_line > len(interpreter_engine.program):
                raise GrinRuntimeError(f"GOTO {target_value} jumps out of bounds.")
            interpreter_engine.current_line = new_line - 1  # Adjust for next increment

        elif isinstance(target_value, str):  # Label jump
            if target_value in interpreter_engine.labels:
                new_line = interpreter_engine.labels[target_value]
                interpreter_engine.current_line = new_line - 1  # Jump to the label's line
            else:
                raise GrinRuntimeError(f'Label "{target_value}" not found.')
        else:
            raise GrinRuntimeError(f'Invalid target type for GOTO: {type(target_value).__name__}')

    def should_jump(self, interpreter_engine):
        """Evaluates the conditional expression, if present."""
        if self.condition_left is None:
            return True  # Unconditional jump

        left = evaluate_expression(self.condition_left, interpreter_engine)
        right = evaluate_expression(self.condition_right, interpreter_engine)
        return compare(left, self.operator, right)

class GotoStatement(JumpStatement):
    """Goto statement class for Grin Goto statements"""
    def execute(self, interpreter_engine):
        value = evaluate_expression(self.target, interpreter_engine)
        if isinstance(value, int):
            if value == 0:
                raise GrinRuntimeError('Cannot jump 0 lines')

        if self.should_jump(interpreter_engine):
            self.jump_to(interpreter_engine)

class GosubStatement(JumpStatement):
    """Gosub statement class for Grin Gosub statements"""
    def execute(self, interpreter_engine):
        if self.should_jump(interpreter_engine):
            interpreter_engine.call_stack.append(interpreter_engine.current_line)  # Save return point
            self.jump_to(interpreter_engine)

class ReturnStatement(Statement):
    """Return statement class for Grin Return statements"""
    def execute(self, interpreter_engine):
        if not interpreter_engine.call_stack:
            raise GrinRuntimeError("RETURN statement encountered without a matching GOSUB.")
        interpreter_engine.current_line = interpreter_engine.call_stack.pop()

class LabelStatement(Statement):
    """Label statement class for Grin Label statements"""
    def __init__(self, label):
        self.label = label

    def execute(self, interpreter_engine):
        pass


__all__ = [
    compare.__name__,
    JumpStatement.__name__,
    GotoStatement.__name__,
    GosubStatement.__name__,
    ReturnStatement.__name__,
    LabelStatement.__name__
]