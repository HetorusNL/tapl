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
    return parsed_args.file


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


def generate_ast(tokens: Stream[Token]) -> AST:
    ast: AST = AstGenerator(tokens).generate()
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


def generate_code(ast: AST, build_folder: Path, header_folder: Path) -> list[str]:
    c_code: list[str] = CodeGenerator(ast, build_folder, header_folder).generate_c()
    print("``` c")
    print(*c_code, sep="", end="")
    print("```")
    return c_code


def write_file(c_code: list[str], build_folder: Path) -> Path:
    # create the full filename of the c source file
    c_file: Path = build_folder / "main.c"
    # write all lines to the file
    with open(c_file, "w") as f:
        f.writelines(c_code)
    return c_file


def compile_c(c_file: Path, build_folder: Path) -> Path:
    # directly call the gcc compiler, passing the build folder as additional include path
    executable: Path = c_file.parent / "main"
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
    ast: AST = generate_ast(tokens)

    # formulate the path to output the c-code, and a subfolder for the headers
    build_folder, header_folder = create_build_folders()

    # generate c-code from the AST
    c_code: list[str] = generate_code(ast, build_folder, header_folder)

    # write the code to main.c in the build folder
    c_file: Path = write_file(c_code, build_folder)

    # run the c compiler to compile the file
    executable: Path = compile_c(c_file, build_folder)

    # run the executable
    run_executable(executable)


if __name__ == "__main__":
    main()
