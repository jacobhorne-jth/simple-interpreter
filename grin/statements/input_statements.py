from grin.statements.basic_statements import Statement
from grin.interpreter.errors import GrinRuntimeError

class InputStatement(Statement):
    """Base class for all Grin Input statements"""
    def __init__(self, var):
        self.var = var

    def execute(self, interpreter_engine):
        raise NotImplementedError

class InnumStatement(InputStatement):
    """Innum statement class for Grin Innum statements"""
    def execute(self, interpreter_engine):
        try:
            input_value = input().strip()
            if "." in input_value:
                first, second = input_value.split('.')
                if first:
                    interpreter_engine.variables[self.var.text()] = float(
                input_value)
                else:
                    raise GrinRuntimeError(f'{input_value} needs to have an integer literal before the decimal place')
            else:
                interpreter_engine.variables[self.var.text()] = int(input_value)

        except ValueError:
            raise GrinRuntimeError(f'Invalid numeric input for {self.var.text()}')

class InstrStatement(InputStatement):
    """Instr statement class for Grin Instr statements"""
    def execute(self, interpreter_engine):
        interpreter_engine.variables[self.var.text()] = input().strip()

__all__ = [
    InputStatement.__name__,
    InnumStatement.__name__,
    InstrStatement.__name__,
]