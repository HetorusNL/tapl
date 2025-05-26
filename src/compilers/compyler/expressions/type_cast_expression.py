#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .expression import Expression
from ..tokens.type_token import TypeToken


class TypeCastExpression(Expression):
    def __init__(self, cast_to: TypeToken, expression: Expression):
        super().__init__()
        self._cast_to: TypeToken = cast_to
        self._expression: Expression = expression

    @property
    def cast_to(self) -> TypeToken:
        return self._cast_to

    @cast_to.setter
    def cast_to(self, cast_to: TypeToken) -> None:
        self._cast_to: TypeToken = cast_to

    @property
    def expression(self) -> Expression:
        return self._expression

    @expression.setter
    def expression(self, expression: Expression) -> None:
        self._expression: Expression = expression

    def c_code(self) -> str:
        return f"(({self.cast_to.type_.keyword}){self.expression})"

    def __str__(self) -> str:
        return f"({self.cast_to.type_.keyword}){self.expression}"

    def __repr__(self) -> str:
        return f"<TypeCastExpression ({self.cast_to.type_.keyword}){self.expression}>"
