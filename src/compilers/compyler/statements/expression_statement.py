#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        super().__init__()
        self._expression: Expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression

    @expression.setter
    def expression(self, expression: Expression) -> None:
        self._expression = expression

    def c_code(self) -> str:
        expression_code: str = self.expression.c_code()

        return f"{expression_code};"

    def __str__(self) -> str:
        return self.expression.__str__()

    def __repr__(self) -> str:
        return f"<ExpressionStatement {self.expression.__repr__()}>"
