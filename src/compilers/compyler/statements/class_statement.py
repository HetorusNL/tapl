#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .function_statement import FunctionStatement
from .lifecycle_statement import LifecycleStatement
from .lifecycle_statement_type import LifecycleStatementType
from .statement import Statement
from .var_decl_statement import VarDeclStatement
from ..tokens.type_token import TypeToken
from ..utils.source_location import SourceLocation


class ClassStatement(Statement):
    def __init__(self, name: TypeToken, source_location: SourceLocation):
        super().__init__(source_location)
        self.name: TypeToken = name
        # store everything that can be in a class statement in the class
        self.variables: list[VarDeclStatement] = []
        self.functions: list[FunctionStatement] = []
        # start with a default/empty constructor and destructor
        self.constructor: LifecycleStatement | None = None
        self.destructor: LifecycleStatement | None = None

    def c_code(self) -> str:
        """returns the full class as a struct"""
        # start with the typedef
        code: str = f"typedef struct {self.name}_struct {self.name};\n"

        # add the class name
        code += f"struct {self.name}_struct {{\n"

        # add all variables
        for variable in self.variables:
            code += f"{variable.c_code()}"

        # end with the closing bracket
        code += f"}};\n"

        # add the constructor, or an empty constructor if there isn't any
        constructor: LifecycleStatement = self.constructor or LifecycleStatement(
            LifecycleStatementType.CONSTRUCTOR, self.name.type_, self.source_location
        )
        code += f"{constructor.c_code()}\n"

        # add the destructor or an empty destructor if there isn't any
        destructor: LifecycleStatement = self.destructor or LifecycleStatement(
            LifecycleStatementType.DESTRUCTOR, self.name.type_, self.source_location
        )
        code += f"{destructor.c_code()}\n"

        # add the methods to the class
        for method in self.functions:
            code += f"{method.c_code()}"

        return code

    def __str__(self) -> str:
        return f"class {self.name}: ..."

    def __repr__(self) -> str:
        return f"<ClassStatement, location {self.source_location}, class {self.name}>"
