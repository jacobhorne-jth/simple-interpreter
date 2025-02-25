from grin.token import GrinToken, GrinTokenKind
from grin.errors import GrinRuntimeError, GrinParseError


def statement_creator(token: list[GrinToken]) -> "Statement":
    """Parses tokens into corresponding statement objects."""
    pass


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
                    #Label statement implementation when label statement class is created
                    #statements.append([(LabelStatement(label_name)), statement])
                except GrinParseError as e:
                    raise GrinParseError(f"Error after label {label_name}: {e}")
        else:
            statements.append(statement_creator(tokens))
        return statements




