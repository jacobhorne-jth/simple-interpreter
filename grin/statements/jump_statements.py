from grin import Statement, GrinRuntimeError, GrinTokenKind

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

class LabelStatement(Statement):
    """Label statement class for Grin Label statements"""
    def __init__(self, label):
        self.label = label

    def execute(self, interpreter_engine):
        pass


__all__ = [
    LabelStatement.__name__,
    compare.__name__
]