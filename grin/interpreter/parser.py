from grin.token import GrinTokenKind, GrinToken
from grin.interpreter.errors import GrinParseError
from grin.statements.basic_statements import LetStatement, PrintStatement, EndStatement
from grin.statements.input_statements import InnumStatement, InstrStatement
from grin.statements.math_statements import AddStatement, SubStatement, MultStatement, DivStatement
from grin.statements.jump_statements import GotoStatement, GosubStatement, LabelStatement, ReturnStatement

def statement_creator(token: list[GrinToken]) -> "Statement":
    """Parses tokens into corresponding statement objects."""
    if not token:
        raise GrinParseError("Empty statement encountered.")

    # Handle GOTO and GOSUB separately because they can be conditional
    if token[0].kind() in {GrinTokenKind.GOTO, GrinTokenKind.GOSUB}:
        target_token = token[1]

        # Check for conditional jump (IF condition is present)
        if len(token) > 2 and token[2].kind() == GrinTokenKind.IF:
            return GotoStatement(
                target=target_token,
                condition_left=token[3],
                operator=token[4],
                condition_right=token[5],
            ) if token[0].kind() == GrinTokenKind.GOTO else GosubStatement(
                target=target_token,
                condition_left=token[3],
                operator=token[4],
                condition_right=token[5],
            )

        # Unconditional jump
        return GotoStatement(target=target_token) if token[0].kind() == GrinTokenKind.GOTO else GosubStatement(
            target=target_token
        )

    # Dictionary mapping tokens to their corresponding statement classes
    statement_classes = {
        GrinTokenKind.LET: LetStatement,
        GrinTokenKind.PRINT: PrintStatement,
        GrinTokenKind.INNUM: InnumStatement,
        GrinTokenKind.INSTR: InstrStatement,
        GrinTokenKind.ADD: AddStatement,
        GrinTokenKind.SUB: SubStatement,
        GrinTokenKind.MULT: MultStatement,
        GrinTokenKind.DIV: DivStatement,
        GrinTokenKind.RETURN: ReturnStatement,
        GrinTokenKind.END: EndStatement,
    }

    # Create an instance of the corresponding statement class
    kind = token[0].kind()
    if kind in statement_classes:
        return statement_classes[kind](*token[1:])

    # If the statement is a label (e.g., `LABEL:`), return a LabelStatement
    if len(token) >= 2 and token[1].kind() == GrinTokenKind.COLON:
        return LabelStatement(token[0].text())

    raise GrinParseError(f"Unknown statement: {token[0].text()}")

def parse_statements_into_objects(token_list: list[list[GrinToken]]) -> list:
    """Parses a list of tokenized statements into Statement objects, handling labels correctly."""
    statements = []
    for tokens in token_list:
        # Check if the line starts with a label
        if (len(tokens) >= 2 and
                tokens[0].kind() == GrinTokenKind.IDENTIFIER and
                tokens[1].kind() == GrinTokenKind.COLON):
            label_name = tokens[0].text()

            remaining_tokens = tokens[2:]

            if remaining_tokens:
                try:
                    statement = statement_creator(remaining_tokens)
                    statements.append([(LabelStatement(label_name)), statement])
                except GrinParseError as e:
                    raise GrinParseError(f"Error after label {label_name}: {e}")
        else:
            statements.append(statement_creator(tokens))
    return statements

__all__ = [
    statement_creator.__name__,
    parse_statements_into_objects.__name__
]