# project3.py
#
# ICS 33 Winter 2025
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

from grin.parsing import parse


def main() -> None:
    statement_list = []
    try:
        while True:
            statement = input()
            if statement.strip() == ".":
                break
            statement_list.append(statement)

        parsed_statements = list(parse(statement_list))
    except Exception as e:
        print(str(e))




if __name__ == '__main__':
    main()
