import argparse

from .ast_generator import AstGenerator
from .tokenizer import Tokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parsed_args = parser.parse_args()
    print(f"calling the compiler with file '{parsed_args.file}'")
    tokens = Tokenizer(parsed_args.file).tokenize()
    print(tokens)
    ast = AstGenerator(tokens).generate()
    print(*ast, sep="\n")


if __name__ == "__main__":
    main()
