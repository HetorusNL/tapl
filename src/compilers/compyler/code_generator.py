#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .utils.ast import AST


class CodeGenerator:
    def __init__(self, ast: AST):
        self._ast = ast

    def generate_c(self) -> list[str]:
        # add the initial lines of code
        c_code: list[str] = [
            "#include <stdbool.h>\n",
            "#include <stdint.h>\n",
            "#include <stdio.h>\n",
            "\n",
            "// TODO: move these to a separate file\n",
            # TODO: extract these types from the Types builtin types
            "typedef uint16_t u16;\n",
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
