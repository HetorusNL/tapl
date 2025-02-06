import argparse
from os import system
from pathlib import Path

from .ast_generator import AstGenerator
from .code_generator import CodeGenerator
from .tokenizer import Tokenizer
from .tokens import Token
from .utils import AST
from .utils import Stream


def argument_parser() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parsed_args = parser.parse_args()
    return parsed_args.file


def tokenize(file: Path) -> Stream[Token]:
    print(f"calling the compiler with file '{file}'")
    tokens: Stream[Token] = Tokenizer(file).tokenize()
    print(tokens.objects)
    return tokens


def generate_ast(tokens: Stream[Token]) -> AST:
    ast: AST = AstGenerator(tokens).generate()
    print(*ast.statements.objects, sep="\n")
    return ast


def generate_code(ast: AST) -> list[str]:
    c_code: list[str] = CodeGenerator(ast).generate_c()
    print("``` c")
    print(*c_code, sep="", end="")
    print("```")
    return c_code


def write_file(c_code: list[str]) -> Path:
    # get to the repo root folder, several levels up
    repo_root: Path = Path(__file__).parents[3].resolve()
    build_folder: Path = repo_root / "build" / "compyler"
    # ensure the build folder exists
    build_folder.mkdir(parents=True, exist_ok=True)
    # create the full filename of the c source file
    c_file: Path = build_folder / "main.c"
    # write all lines to the file
    with open(c_file, "w") as f:
        f.writelines(c_code)
    return c_file


def compile_c(c_file: Path) -> Path:
    executable: Path = c_file.parent / "main"
    command: str = f"gcc -o {executable} {c_file}"
    print(command)
    system(command)
    return executable


def run_executable(executable: Path):
    print(executable)
    system(executable)


def main():
    # get the 'file' argument from the argument parser
    file: Path = argument_parser()

    # tokenize the provided file
    tokens: Stream[Token] = tokenize(file)

    # generate an AST from the tokens
    ast: AST = generate_ast(tokens)

    # generate c-code from the AST
    c_code: list[str] = generate_code(ast)

    # write the code to main.c in the build folder
    c_file: Path = write_file(c_code)

    # run the c compiler to compile the file
    executable: Path = compile_c(c_file)

    # run the executable
    run_executable(executable)


if __name__ == "__main__":
    main()
