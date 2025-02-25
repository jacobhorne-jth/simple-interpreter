from grin.parsing import parse
from grin.interpreter.engine import InterpreterEngine
from grin.interpreter.parser import parse_statements_into_objects


def main() -> None:
    statement_list = []
    try:
        while True:
            statement = input()
            if statement.strip() == ".":
                break
            statement_list.append(statement)
        parsed_statements = list(parse(statement_list))
        parsed_objects = parse_statements_into_objects(parsed_statements)
        engine = InterpreterEngine(parsed_objects)
        engine.run()

    except Exception as e:
        print(str(e))



if __name__ == '__main__':
    main()