#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from ..tokens.identifier_token import IdentifierToken


class CallExpression(Expression):
    def __init__(self, name: IdentifierToken, arguments: list[Expression] = []):
        super().__init__()
        self._name: IdentifierToken = name
        self._arguments: list[Expression] = arguments

    @property
    def name(self) -> IdentifierToken:
        return self._name

    @name.setter
    def name(self, name: IdentifierToken) -> None:
        self._name: IdentifierToken = name

    @property
    def arguments(self) -> list[Expression]:
        return self._arguments

    @arguments.setter
    def arguments(self, arguments: list[Expression]) -> None:
        self._arguments: list[Expression] = arguments

    def c_code(self) -> str:
        arguments: str = ", ".join([argument.c_code() for argument in self.arguments])
        return f"{self.name}({arguments})"

    def __str__(self) -> str:
        return f'{self.name.value}({", ".join([argument.__str__() for argument in self.arguments])})'

    def __repr__(self) -> str:
        return f"<CallExpression {self.name.value}>"
