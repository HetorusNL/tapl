#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement


class PrintStatement(Statement):
    def __init__(self, value: Expression):
        super().__init__()
        self._value: Expression = value

    @property
    def value(self) -> Expression:
        return self._value

    @value.setter
    def value(self, value: Expression) -> None:
        self._value: Expression = value

    def c_code(self) -> str:
        expression: str = self.value.c_code()

        return f'printf("%d\\n", {expression});'

    def __str__(self) -> str:
        return f"print({self.value.__str__()})"

    def __repr__(self) -> str:
        return f"<PrintStatement {self.value.__repr__()}>"
