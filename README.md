# simple-interpreter
A Python interpreter for the Grin custom-designed programming language, executing custom scripts with variables, arithmetic, control flow, and I/O.

**Overview**

This project implements a fully functional interpreter for Grin, a small, custom-designed programming language. Built in Python, the interpreter processes Grin source code—parsing, evaluating, and executing statements in sequence—while supporting arithmetic operations, variables, control flow, and basic input/output.

The project emphasizes:

- Object-oriented design: Statements and values are modeled as classes.

- Modularity: Lexing, parsing, execution, and error handling are cleanly separated across modules.

- Robustness: Extensive unit tests ensure correctness across a variety of scenarios.

- Educational value: Grin was created to illustrate the core principles behind how interpreters work.

  Note: Grin is a fictional language designed purely for learning purposes.

**Grin Language Overview**

Grin programs are sequences of statements, each on its own line. Execution starts at the first line and ends when an END statement or a . marker is encountered.

_Example Grin Program:_
<br>
```text
LET MESSAGE "Hello World!"
PRINT MESSAGE
.
```

Output:
```text
Hello World!
```

_Key Features of Grin:_

- Variables: Store integers, floats, or strings.

- Arithmetic: ADD, SUB, MULT, DIV to modify variable values.

- Input: INNUM reads numeric input; INSTR reads string input.

- Control Flow: GOTO and GOSUB for jumping and subroutines.

- Conditionals: Optional IF clauses with comparison operators (=, <, >, etc.).

- Subroutines: GOSUB + RETURN provide reusable code blocks.

- Labels: Lines can be marked and referenced by name.

**Project Features**

- Lexer and Parser

    Tokenizes Grin source code into lexemes and parses them into executable statements.

- Execution Engine

    Sequentially processes statements and maintains interpreter state (variables, labels, call stack).

- Arithmetic and String Operations

    Supports mixed-type arithmetic and string concatenation/repetition.

- Control Flow

    Conditional and unconditional jumps and subroutines.

- Error Handling

    Gracefully terminates on syntax or runtime errors.

- Unit Tests

    Extensive test coverage across modules for correctness and stability.

**How to Run**

_Prerequisites_

- Python 3.6+

_Running the Interpreter_

  python3 interpretermain.py

_Usage_

- The interpreter will wait for Grin program input.

- Enter statements line by line.

- End the program input with a single . on a line by itself.

- Outputs and any errors will be printed to the console.

**Example Session**
```text
LET X 5
ADD X 3
PRINT X
.
```
Output:
```text
8
```
<br>

**Project Structure**

```text
simple-interpreter/
├── interpretermain.py         # Entry point to launch the interpreter
├── grin/                      # Main Grin package
│   ├── __init__.py
│   ├── engine.py              # Core execution engine
│   ├── errors.py              # Custom error types
│   ├── lexing.py              # Tokenizer (lexer)
│   ├── location.py            # Source code position tracking
│   ├── parser.py              # Parser logic
│   ├── parsing.py             # Parsing helpers
│   ├── token.py               # Token definitions
│   └── statements/            # Statement implementations
│       ├── __init__.py
│       ├── basic_statements.py    # LET, PRINT, END
│       ├── input_statements.py    # INNUM, INSTR
│       ├── jump_statements.py     # GOTO, GOSUB, RETURN
│       └── math_statements.py     # ADD, SUB, MULT, DIV
└── tests/                     # Unit tests
    ├── grin/
    │   ├── test_engine.py
    │   ├── test_parser.py
    │   ├── test_lexing.py
    │   ├── test_location.py
    │   └── test_token.py
    ├── statements/
    │   ├── test_basic_statements.py
    │   ├── test_input_statements.py
    │   ├── test_jump_statements.py
    │   └── test_math_statements.py
    └── test_interpretermain.py
```
<br>

**Sample Grin Programs**

_Arithmetic and Variables:_
```text
LET A 4
LET B 3
MULT A B
PRINT A
.
```
Output:
```text
12
```

Conditional GOTO:
```text
LET N 5
GOTO 2 IF N > 3
PRINT "This won't print."
PRINT "This will print."
.
```
Output:
```text
This will print.
```

Subroutines:
```text
LET X 1
GOSUB "DOUBLER"
PRINT X
END
DOUBLER: MULT X 2
RETURN
.
```
Output:
```text
2
```

_Notes_

- The interpreter was designed for clarity and educational value, not for production use.

- Grin's syntax is intentionally simplified compared to real-world languages.

_Future Enhancements_

- Add support for user-defined functions with parameters.

- Extend expression parsing for complex arithmetic.

- Implement a REPL mode for interactive execution.

<br>


_License_
<br>
- This project is intended for educational use.

