import argparse

from .ast import AST
from .tokenizer import Tokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parsed_args = parser.parse_args()
    print(f"calling the compiler with file '{parsed_args.file}'")
    tokens = Tokenizer(parsed_args.file).tokenize()
    print(tokens)
    ast = AST(tokens).generate()
    print(ast)


if __name__ == "__main__":
    main()
