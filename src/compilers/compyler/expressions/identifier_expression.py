#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .expression import Expression
from ..utils.source_location import SourceLocation
from ..tokens.identifier_token import IdentifierToken


class IdentifierExpression(Expression):
    def __init__(self, source_location: SourceLocation, identifier_token: IdentifierToken):
        super().__init__(source_location)
        self.identifier_token: IdentifierToken = identifier_token
        self.inner_expression: Expression | None = None

    def c_code(self) -> str:
        if self.inner_expression:
            return f"{self.identifier_token}.{self.inner_expression.c_code()}"
        else:
            return f"{self.identifier_token}"

    def __str__(self) -> str:
        if self.inner_expression:
            return f"{self.identifier_token}.{self.inner_expression}"
        else:
            return f"{self.identifier_token}"

    def __repr__(self) -> str:
        string: str = f"<IdentifierExpression: location {self.source_location}, {self.identifier_token}"
        if self.inner_expression:
            string = f"{string}.{self.inner_expression}"
        string = f"{string}>"
        return string
