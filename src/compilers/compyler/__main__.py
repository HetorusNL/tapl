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


def typing_passes(tokens: Stream[Token]):
    # resolve the types in the file
    type_resolver: TypeResolver = TypeResolver(tokens)
    types: Types = type_resolver.resolve()
    # apply the types to the tokens in the stream
    type_applier: TypeApplier = TypeApplier(types)
    type_applier.apply(tokens)
    # return the processed tokens
    return tokens


def generate_ast(file: Path, tokens: Stream[Token]) -> AST:
    ast: AST = AstGenerator(file, tokens).generate()
    print(*ast.statements.objects, sep="\n")
    return ast


def create_build_folders() -> tuple[Path, Path]:
    # get to the repo root folder, several levels up
    repo_root: Path = Path(__file__).parents[3].resolve()
    build_folder: Path = repo_root / "build" / "compyler"
    header_folder: Path = build_folder / "tapl_headers"
    # ensure the build and header folders exists
    build_folder.mkdir(parents=True, exist_ok=True)
    header_folder.mkdir(parents=True, exist_ok=True)
    return build_folder, header_folder


def generate_code(ast: AST, build_folder: Path, header_folder: Path) -> Path:
    main_c_file: Path = build_folder / "main.c"
    CodeGenerator(ast, build_folder, header_folder).generate_c(main_c_file)
    return main_c_file


def format_files(folder: Path) -> None:
    # recursively find all .c and .h files in the build folder and format all found files
    for file_path in folder.rglob("*.[ch]"):
        if file_path.is_file():
            command: str = f"clang-format -i --fallback-style=none {file_path}"
            print(command)
            system(command)


def compile_c(c_file: Path, build_folder: Path) -> Path:
    executable: Path = c_file.parent / "main"

    # remove the old executable (if it exists)
    command: str = f"rm -f {executable}"
    print(command)
    system(command)

    # directly call the gcc compiler, passing the build folder as additional include path
    command: str = f"gcc -I{build_folder} -o {executable} {c_file}"
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

    # apply the two typing passes to the token stream
    tokens = typing_passes(tokens)

    # generate an AST from the tokens
    ast: AST = generate_ast(file, tokens)

    # formulate the path to output the c-code, and a subfolder for the headers
    build_folder, header_folder = create_build_folders()

    # generate c-code from the AST and write the source files in the build folder
    c_file: Path = generate_code(ast, build_folder, header_folder)

    # format the generated c-code files
    format_files(build_folder)

    # run the c compiler to compile the file
    executable: Path = compile_c(c_file, build_folder)

    # run the executable
    run_executable(executable)


if __name__ == "__main__":
    main()
