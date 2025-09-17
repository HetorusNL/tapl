#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from ..tokens.identifier_token import IdentifierToken
from ..utils.source_location import SourceLocation


class CallExpression(Expression):
    def __init__(self, source_location: SourceLocation, name: IdentifierToken, arguments: list[Expression] = []):
        super().__init__(source_location)
        self.name: IdentifierToken = name
        self.arguments: list[Expression] = arguments

    def c_code(self) -> str:
        arguments: str = ", ".join([argument.c_code() for argument in self.arguments])
        return f"{self.name}({arguments})"

    def __str__(self) -> str:
        return f'{self.name.value}({", ".join([argument.__str__() for argument in self.arguments])})'

    def __repr__(self) -> str:
        return f"<CallExpression: location {self.source_location}, {self.name.value}>"
