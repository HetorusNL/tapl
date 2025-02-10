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
            "#include <stdio.h>\n",
            "\n",
            "int main(int argc, char** argv) {\n",
            '    printf("hello world!\\n");\n',
        ]

        # compile the statements in the AST to code
        for index, statement in enumerate(self._ast.statements.objects):
            statement_code: str = statement.c_code()
            c_code.append(
                f'    printf("statement {index+1}: %d\\n", {statement_code});\n'
            )

        # add the ending lines of code
        c_code.append("}\n")

        # return the full source code
        return c_code
