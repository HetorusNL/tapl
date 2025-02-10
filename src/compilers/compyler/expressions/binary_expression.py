#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .expression import Expression
from .token_expression import TokenExpression
from ..tokens.token import Token


class BinaryExpression(TokenExpression):
    def __init__(self, left: Expression, token: Token, right: Expression):
        super().__init__(token)
        self._left: Expression = left
        self._right: Expression = right

    @property
    def left(self) -> Expression:
        return self._left

    @left.setter
    def left(self, left: Expression) -> None:
        self._left: Expression = left

    @property
    def right(self) -> Expression:
        return self._right

    @right.setter
    def right(self, right: Expression) -> None:
        self._right: Expression = right

    def c_code(self) -> str:
        left_code: str = self.left.c_code()
        token_code: str = self.token.token_type.value
        right_code: str = self.right.c_code()
        return f"({left_code} {token_code} {right_code})"

    def __str__(self) -> str:
        return f"({self.left} {self.token.token_type.value} {self.right})"

    def __repr__(self) -> str:
        return f"<BinaryExpression {self.left} {self.token.token_type} {self.right}>"
