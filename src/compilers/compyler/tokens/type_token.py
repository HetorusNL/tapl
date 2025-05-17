#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .token_type import TokenType
from .token import Token
from ..types.type import Type


class TypeToken(Token):
    def __init__(self, line: int, type_: Type):
        super().__init__(TokenType.TYPE, line)
        # sstore the additional properties in the class
        self._type: Type = type_

    @property
    def type_(self) -> Type:
        return self._type

    @type_.setter
    def type_(self, type_: Type) -> None:
        self._type: Type = type_

    def __str__(self) -> str:
        return f"{self._type.keyword}"

    def __repr__(self) -> str:
        return f'<{self.token_type}: line {self.line}, "{self._type.keyword}">'
