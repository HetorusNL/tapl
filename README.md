# TAPL

Repository with the compiler/examples/documentation of TAPL (Tim's Awesome Programming Language).

## Information

Two compilers are created:

- compyler: the bootstrapping compiler, written in python
- compiler: the compiler written in TAPL, compiled using compyler

## Usage

Install the poetry environment for the compyler by running:

```bash
poetry install
```

Currently working on the tokenizer and AST generator of the compyler TAPL compiler.
Run the following command to watch the tokenizer and AST generator using the unittests and `example.tim` files in the test directory, and see the output of the tokenizing and AST generation step:

```bash
poetry run ptw
```

## TODO

- fix open TODOs in `tokenizer.py`
  - add 0b / 0x / e number parsing
  - make distinction between int and float/double numbers
- change `__str__` and `__repr__` implementation so it can be used for unittests
  - e.g. convert `1 + 2 * 3` to `((1) + ((2) * (3)))` or something
- add additional expression stuff to the ast_generator
- start on the code generator
- add statements to the ast_generator
- start on adding typing support
- add language server
  - https://pygls.readthedocs.io/en/latest/servers/getting-started.html
  - example: https://github.com/windelbouwman/sauce-os/tree/main/language-server/slang-lang

## FAQ

## License

MIT License, Copyright (c) 2024 Tim Klein Nijenhuis <tim@hetorus.nl>
