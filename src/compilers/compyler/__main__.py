#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

import argparse
from os import system
from pathlib import Path

from .ast_generator import AstGenerator
from .code_generator import CodeGenerator
from .tokenizer import Tokenizer
from .tokens.token import Token
from .types.type_applier import TypeApplier
from .types.type_resolver import TypeResolver
from .types.types import Types
from .utils.ast import AST
from .utils.stream import Stream
from .ast_checks.ast_check import AstCheck


# get to the repo root folder, several levels up
repo_root: Path = Path(__file__).parents[3].resolve()
stdlib_folder: Path = repo_root / "src" / "stdlib"
templates_folder: Path = repo_root / "src" / "templates"


def argument_parser() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parsed_args = parser.parse_args()
    return Path(parsed_args.file)


def tokenize(file: Path) -> Stream[Token]:
    print(f"calling the compiler with file '{file}'")
    tokens: Stream[Token] = Tokenizer(file).tokenize()
    print(tokens.objects)
    return tokens


def typing_passes(tokens: Stream[Token]) -> Types:
    # resolve the types in the file
    type_resolver: TypeResolver = TypeResolver(tokens)
    types: Types = type_resolver.resolve()
    # apply the types to the tokens in the stream (in place)
    type_applier: TypeApplier = TypeApplier(types)
    type_applier.apply(tokens)
    # return the processed tokens
    return types


def generate_ast(file: Path, tokens: Stream[Token], types: Types) -> AST:
    ast: AST = AstGenerator(file, tokens, types).generate()
    print(*ast.statements.objects, sep="\n")
    return ast


def check_ast(ast: AST) -> None:
    """run several checks on the generated AST"""
    AstCheck(ast).run()


def create_build_folders() -> tuple[Path, Path]:
    build_folder: Path = repo_root / "build" / "compyler"
    header_folder: Path = build_folder / "tapl_headers"
    # ensure the build and header folders exists
    build_folder.mkdir(parents=True, exist_ok=True)
    header_folder.mkdir(parents=True, exist_ok=True)
    return build_folder, header_folder


def generate_code(ast: AST, build_folder: Path, header_folder: Path, templates_folder: Path) -> Path:
    main_c_file: Path = build_folder / "main.c"
    CodeGenerator(ast, build_folder, header_folder, templates_folder).generate_c(main_c_file)
    return main_c_file


def copy_stdlib(header_folder: Path, stdlib_folder: Path) -> None:
    # recursively copy all header files to the header folder
    # using the neat Path.copy_into function, available since python 3.14
    for header in stdlib_folder.glob("*.h"):
        header.copy_into(header_folder)


def format_files(folder: Path) -> None:
    # recursively find all .c and .h files in the build folder and format all found files
    for file_path in folder.rglob("*.[ch]"):
        if file_path.is_file():
            command: str = f"clang-format -i --fallback-style=none {file_path}"
            print(command)
            if error_code := system(command):
                handle_error(f"clang-format failed to format {file_path} with error code {error_code}")


def compile_c(c_file: Path, build_folder: Path) -> Path:
    executable: Path = c_file.parent / "main"

    # remove the old executable (if it exists)
    command: str = f"rm -f {executable}"
    print(command)
    system(command)

    # directly call the gcc compiler, passing the build folder as additional include path
    command: str = f"gcc -O0 -g3 -I{build_folder} -o {executable} {c_file}"
    print(command)
    if error_code := system(command):
        handle_error(f"gcc returned error code {error_code}")
    return executable


def run_executable(executable: Path):
    print(executable)
    system(executable)


def handle_error(error_msg: str):
    # lazy import the inspect and colors modules for error handling
    import inspect
    from inspect import FrameInfo

    from .utils.colors import Colors

    # try to get the line number of the function calling this function
    stack: list[FrameInfo] = inspect.stack()
    line: str = f"{stack[1].lineno}:" if len(stack) >= 2 else ""

    # construct the filename and error message with colors
    filename: str = f"\n{Colors.BOLD}{__file__}:{line} {Colors.RESET}"
    error: str = f"{Colors.BOLD}{Colors.RED}internal compiler error: {Colors.RESET}"

    # print the error and exit with failure
    print(f"{filename}{error}{error_msg}!")
    print(f"{Colors.BOLD}{Colors.MAGENTA}terminating...{Colors.RESET}")
    exit(1)


def main():
    # get the 'file' argument from the argument parser
    file: Path = argument_parser()

    # tokenize the provided file
    tokens: Stream[Token] = tokenize(file)

    # apply the two typing passes to the token stream
    types: Types = typing_passes(tokens)

    # generate an AST from the tokens
    ast: AST = generate_ast(file, tokens, types)

    # run several checks on the generated AST
    check_ast(ast)

    # formulate the path to output the c-code, and a subfolder for the headers
    build_folder, header_folder = create_build_folders()

    # generate c-code from the AST and write the source files in the build folder
    c_file: Path = generate_code(ast, build_folder, header_folder, templates_folder)

    # copy the files in the standard library to the header folder
    copy_stdlib(header_folder, stdlib_folder)

    # format the generated c-code files
    format_files(build_folder)

    # run the c compiler to compile the file
    executable: Path = compile_c(c_file, build_folder)

    # run the executable
    run_executable(executable)


if __name__ == "__main__":
    main()
