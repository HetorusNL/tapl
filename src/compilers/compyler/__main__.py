import argparse

from .ast import AST
from .ast_generator import AstGenerator
from .tokenizer import Tokenizer
from .tokens import Token


def main():
    # get the 'file' argument from the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parsed_args = parser.parse_args()

    # tokenize the provided file
    print(f"calling the compiler with file '{parsed_args.file}'")
    tokens: list[Token] = Tokenizer(parsed_args.file).tokenize()
    print(tokens)

    # generate an AST from the tokens
    ast: AST = AstGenerator(tokens).generate()
    print(*ast.expressions, sep="\n")


if __name__ == "__main__":
    main()
