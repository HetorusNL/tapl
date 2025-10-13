#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from ..expressions.identifier_expression import IdentifierExpression
from ..utils.source_location import SourceLocation


class CallExpression(Expression):
    def __init__(
        self, source_location: SourceLocation, expression: IdentifierExpression, arguments: list[Expression] = []
    ):
        super().__init__(source_location)
        self.expression: IdentifierExpression = expression
        self.arguments: list[Expression] = arguments

    def c_code(self) -> str:
        arguments: str = ", ".join([argument.c_code() for argument in self.arguments])
        return f"{self.expression.c_code()}({arguments})"

    def __str__(self) -> str:
        return f'{self.expression.__str__()}({", ".join([argument.__str__() for argument in self.arguments])})'

    def __repr__(self) -> str:
        return f"<CallExpression: location {self.source_location}, {self.expression.__repr__()}>"
