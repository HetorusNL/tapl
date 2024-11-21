import argparse

from .tokenizer import Tokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parsed_args = parser.parse_args()
    print(f"calling the compiler with file '{parsed_args.file}'")
    print(Tokenizer(parsed_args.file).tokenize())


if __name__ == "__main__":
    main()
