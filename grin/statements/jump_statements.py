from grin.statements.basic_statements import Statement

class LabelStatement(Statement):
    """Label statement class for Grin Label statements"""
    def __init__(self, label):
        self.label = label

    def execute(self, interpreter_engine):
        pass

