# TAPL

Repository with the compiler/examples/documentation of TAPL (Tim's Awesome Programming Language).

## Information

Two compilers are created:

- compyler: the bootstrapping compiler, written in python
- tapl/taplc/compiler: the compiler/REPL written in TAPL, compiled using compyler

## Usage

Install the poetry environment for the compyler by running:

```bash
poetry install
```

Currently working on the tokenizer and AST generator of the compyler TAPL compiler.
Run the following command to watch the tokenizer and AST generator using the unittests and the example `.tim` files in the test directory, and see the output of the tokenizing and AST generation step:

```bash
poetry run ptw
```

Run the following command to compile and run the example with the currently implemented functionality:

```bash
poetry run python -m src.compilers.compyler examples/current_functionality.tim
```

Run the following command to compile and execute any tim file:

```bash
poery run python -m src.compilers.compyler /path/to/file.tim
```

## TODO

- fix open TODOs in `tokenizer.py`
  - add 0o / e number parsing
  - make distinction between int and float/double numbers
- add additional expression stuff to the ast_generator
- add statements to the ast_generator
- add another typing (type propagation / type checking) pass
- add language server
  - https://pygls.readthedocs.io/en/latest/servers/getting-started.html
  - example: https://github.com/windelbouwman/sauce-os/tree/main/language-server/slang-lang

## Ideas

- add public/private to classes, functions
- make everything private by default (classes, functions, members)
- implicit "python modules' class imports", example:
  - `modules/some_module.tim`: `class SomeModule: // blabla`
  - `file.tim`: `from module import SomeModule`
- add `returnif` keyword-like thing:

  - an indented block of statements follow this
  - if a statement returns a non-null value, return this from the surrounding function
  - example:

    ```
    Statement statement():
        // very neatly functions returning if they are non-null
        returnif:
            if_statement()
            for_statement()
            print_statement()

        // outside of the block use a normal return statement
        Expression e = expression()
        return ExpressionStatement(e)
    ```

## FAQ

## License

MIT License, Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
