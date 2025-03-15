#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement
from ..tokens.identifier_token import IdentifierToken


class AssignmentStatement(Statement):
    def __init__(self, identifier_token: IdentifierToken, value: Expression):
        super().__init__()
        self._identifier_token: IdentifierToken = identifier_token
        self._value: Expression = value

    @property
    def identifier_token(self) -> IdentifierToken:
        return self._identifier_token

    @identifier_token.setter
    def identifier_token(self, identifier_token: IdentifierToken) -> None:
        self._identifier_token: IdentifierToken = identifier_token

    @property
    def value(self) -> Expression:
        return self._value

    @value.setter
    def value(self, value: Expression) -> None:
        self._value: Expression = value

    def c_code(self) -> str:
        identifier: str = self.identifier_token.value
        value: str = self.value.c_code()

        return f"{identifier} = {value};"
