#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from .utils.ast import AST
from .types.types import Types


class CodeGenerator:
    def __init__(self, ast: AST, build_folder: Path, header_folder: Path):
        self._ast: AST = ast
        self._build_folder: Path = build_folder
        self._header_folder: Path = header_folder

    def generate_c(self) -> list[str]:
        # also generate the typedefs for all builtin basic types
        Types().generate_c_header(self._header_folder)

        # add the initial lines of code
        c_code: list[str] = [
            "// include the needed system headers\n",
            "#include <stdio.h>\n",
            "\n",
            "// also include the needed TAPL headers\n",
            "#include <tapl_headers/types.h>\n",
            "\n",
            "int main(int argc, char** argv) {\n",
            '    printf("hello world!\\n");\n',
        ]

        # compile the statements in the AST to code
        for statement in self._ast.statements.objects:
            statement_code: str = statement.c_code()
            c_code.append(f"    {statement_code}\n")

        # add the ending lines of code
        c_code.append("}\n")

        # return the full source code
        return c_code
