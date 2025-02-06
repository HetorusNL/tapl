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
- start on adding typing support
  - add type resolver that resolves class declarations (and more?) for types
  - add second type pass that 'attaches' types to variable (declarations)
- add language server
  - https://pygls.readthedocs.io/en/latest/servers/getting-started.html
  - example: https://github.com/windelbouwman/sauce-os/tree/main/language-server/slang-lang

## FAQ

## License

MIT License, Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
