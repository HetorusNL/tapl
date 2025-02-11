#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .token_type import TokenType
from .token import Token
from ..types.type import Type


class VarDeclToken(Token):
    def __init__(self, line: int, var_type: Type, name: str):
        super().__init__(TokenType.VAR_DECL, line)
        # store the additional properties in the class
        self._var_type: Type = var_type
        self._name: str = name

    @property
    def var_type(self) -> Type:
        return self._var_type

    @var_type.setter
    def var_type(self, var_type: Type) -> None:
        self._var_type = var_type

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def __str__(self) -> str:
        return f"{self.var_type.keyword} {self.name}"

    def __repr__(self) -> str:
        content: str = f"{self.var_type.keyword} {self.name}"
        return f'<{self.token_type}: line {self.line}, "{content}">'
