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

Currently working on the tokenizer of the compyler TAPL compiler.
Run the following command to watch the tokenizer using the tokenizer unittest and `example.tim` file, and see the output of the tokenizing step:

```bash
poetry run ptw
```

## FAQ

## License

MIT License, Copyright (c) 2024 Tim Klein Nijenhuis <tim@hetorus.nl>
