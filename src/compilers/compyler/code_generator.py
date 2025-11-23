#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from .utils.ast import AST
from .statements.class_statement import ClassStatement
from .statements.function_statement import FunctionStatement


class CodeGenerator:
    def __init__(self, ast: AST, build_folder: Path, header_folder: Path, templates_folder: Path):
        self._ast: AST = ast
        self._build_folder: Path = build_folder
        self._header_folder: Path = header_folder
        self._templates_folder: Path = templates_folder

    def generate_c(self, main_c_file: Path) -> None:
        # also generate the typedefs for all builtin basic types
        self._ast.types.generate_c_headers(self._header_folder, self._templates_folder)

        class_c_definitions: list[str] = []
        function_c_declarations: list[str] = []
        function_c_definitions: list[str] = []
        main_c_lines: list[str] = []

        # compile the statements in the AST to code
        for statement in self._ast.statements.objects:
            if isinstance(statement, ClassStatement):
                class_c_definitions.append(f"{statement.c_code()}\n")
            elif isinstance(statement, FunctionStatement):
                function_c_declarations.append(f"{statement.c_declaration()}\n")
                function_c_definitions.append(f"{statement.c_code()}\n")
            else:
                main_c_lines.append(f"{statement.c_code()}\n")

        # write the classes to the classes c file
        self._write_classes_c(class_c_definitions)

        # write the functions to the functions c file
        self._write_functions_c(function_c_declarations, function_c_definitions)

        # write the main c file with the code
        self._write_main_c_file(main_c_lines, main_c_file)

    def _write_classes_c(self, definitions: list[str]):
        classes_c_file: Path = self._header_folder / "classes.h"

        initial_lines: list[str] = [
            "#pragma once\n",
            "\n",
            "// include the needed system headers\n",
            "#include <stdio.h>\n",
            "\n",
            "// also include the needed TAPL headers\n",
            "#include <tapl_headers/types.h>\n",
            "\n",
            "// classes declarations\n",
        ]

        with open(classes_c_file, "w") as f:
            f.writelines(initial_lines)
            f.writelines(definitions)

    def _write_functions_c(self, declarations: list[str], definitions: list[str]):
        functions_c_file: Path = self._header_folder / "functions.h"

        initial_lines: list[str] = [
            "#pragma once\n",
            "\n",
            "// include the needed system headers\n",
            "#include <stdio.h>\n",
            "\n",
            "// also include the needed TAPL headers\n",
            "#include <tapl_headers/types.h>\n",
            "\n",
            "// function declarations\n",
        ]
        definition_lines: list[str] = [
            "\n",
            "// function definitions\n",
        ]

        with open(functions_c_file, "w") as f:
            f.writelines(initial_lines)
            f.writelines(declarations)
            f.writelines(definition_lines)
            f.writelines(definitions)

    def _write_main_c_file(self, code_lines: list[str], c_file: Path) -> None:
        initial_lines: list[str] = [
            "// include the needed system headers\n",
            "#include <stdio.h>\n",
            "\n",
            "// also include the needed TAPL headers\n",
            "#include <tapl_headers/classes.h>\n",
            "#include <tapl_headers/functions.h>\n",
            "#include <tapl_headers/list.h>\n",
            "#include <tapl_headers/types.h>\n",
            "\n",
            "int main(int argc, char** argv) {\n",
            'printf("hello world!\\n");\n',
        ]

        with open(c_file, "w") as f:
            f.writelines(initial_lines)
            f.writelines(code_lines)
            f.write("}\n")
