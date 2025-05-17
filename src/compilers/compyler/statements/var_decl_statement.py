#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement
from ..tokens.identifier_token import IdentifierToken
from ..tokens.type_token import TypeToken


class VarDeclStatement(Statement):
    def __init__(self, type_token: TypeToken, name: IdentifierToken, initial_value: Expression | None = None):
        super().__init__()
        self._type_token: TypeToken = type_token
        self._name: IdentifierToken = name
        self._initial_value: Expression | None = initial_value

    @property
    def type_token(self) -> TypeToken:
        return self._type_token

    @type_token.setter
    def type_token(self, type_token: TypeToken) -> None:
        self._type_token: TypeToken = type_token

    @property
    def name(self) -> IdentifierToken:
        return self._name

    @name.setter
    def name(self, name: IdentifierToken) -> None:
        self._name: IdentifierToken = name

    @property
    def initial_value(self) -> Expression | None:
        return self._initial_value

    @initial_value.setter
    def initial_value(self, initial_value: Expression | None) -> None:
        self._initial_value: Expression | None = initial_value

    def c_code(self) -> str:
        keyword: str = self.type_token.type_.keyword
        name: str = self.name.value

        # if we have an initial value, also generate code for that
        if self.initial_value:
            initial_value: str = self.initial_value.c_code()
            return f"{keyword} {name} = {initial_value};"

        # otherwise it's a default initialized variable
        return f"{keyword} {name};"

    def __str__(self) -> str:
        return f"{self.type_token.type_.keyword} {self.name.value}"

    def __repr__(self) -> str:
        return f"<VarDeclStatement {self.type_token.type_.keyword} {self.name.value}"
