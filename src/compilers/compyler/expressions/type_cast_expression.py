#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .expression import Expression
from ..tokens.type_token import TypeToken
from ..utils.source_location import SourceLocation


class TypeCastExpression(Expression):
    def __init__(self, source_location: SourceLocation, cast_to: TypeToken, expression: Expression):
        super().__init__(source_location)
        self.cast_to: TypeToken = cast_to
        self.expression: Expression = expression

    def c_code(self) -> str:
        return f"(({self.cast_to.c_code()}){self.expression.c_code()})"

    def __str__(self) -> str:
        return f"({self.cast_to}){self.expression}"

    def __repr__(self) -> str:
        return f"<TypeCastExpression: location {self.source_location}, ({self.cast_to}){self.expression}>"
