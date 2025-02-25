from grin import GrinToken, GrinTokenKind, GrinParseError, LetStatement, PrintStatement, \
    EndStatement, LabelStatement, AddStatement, InnumStatement, InstrStatement, SubStatement, \
    MultStatement, DivStatement


def statement_creator(token: list[GrinToken]) -> "Statement":
    """Parses tokens into corresponding statement objects."""
    if not token:
        raise GrinParseError("Empty statement encountered.")

    # Dictionary mapping tokens to their corresponding statement classes
    statement_classes = {
        GrinTokenKind.LET: LetStatement,
        GrinTokenKind.PRINT: PrintStatement,
        GrinTokenKind.END: EndStatement,
        GrinTokenKind.INNUM: InnumStatement,
        GrinTokenKind.INSTR: InstrStatement,
        GrinTokenKind.ADD: AddStatement,
        GrinTokenKind.SUB: SubStatement,
        GrinTokenKind.MULT: MultStatement,
        GrinTokenKind.DIV: DivStatement
    }

    # Create an instance of the corresponding statement class
    kind = token[0].kind()
    if kind in statement_classes:
        return statement_classes[kind](*token[1:])

    # If the statement is a label return a LabelStatement
    if len(token) >= 2 and token[1].kind() == GrinTokenKind.COLON:
        return LabelStatement(token[0].text())

    raise GrinParseError(f"Unknown statement: {token[0].text()}")


def parse_statements_into_objects(token_list: list[list[GrinToken]]) -> list:
    """Parses a list of tokenized statements into Statement objects, handling labels correctly."""
    statements = []
    for tokens in token_list:
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

