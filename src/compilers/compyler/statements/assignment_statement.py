#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement
from ..tokens.identifier_token import IdentifierToken
from ..utils.source_location import SourceLocation


class AssignmentStatement(Statement):
    def __init__(self, identifier_token: IdentifierToken, value: Expression):
        source_location: SourceLocation = identifier_token.source_location + value.source_location
        super().__init__(source_location)
        self.identifier_token: IdentifierToken = identifier_token
        self.value: Expression = value

    def c_code(self) -> str:
        identifier: str = self.identifier_token.value
        value: str = self.value.c_code()

        return f"{identifier} = {value};"

    def __str__(self) -> str:
        identifier: str = self.identifier_token.value
        value: str = self.value.__str__()

        return f"{identifier} = {value}"

    def __repr__(self) -> str:
        identifier: str = self.identifier_token.value
        value: str = self.value.__repr__()

        return f"<AssignmantStatement: location {self.source_location}, {identifier} = {value}>"
