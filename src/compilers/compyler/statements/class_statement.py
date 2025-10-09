#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .function_statement import FunctionStatement
from .lifecycle_statement import LifecycleStatement
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
        self.constructor: LifecycleStatement | None = None
        self.destructor: LifecycleStatement | None = None

    def __str__(self) -> str:
        return f"class {self.name.type_.keyword}: ..."

    def __repr__(self) -> str:
        return f"<ClassStatement, location {self.source_location}, class {self.name.type_.keyword}>"
