#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement


class ReturnStatement(Statement):
    def __init__(self, value: Expression | None = None):
        super().__init__()
        self._value: Expression | None = value

    @property
    def value(self) -> Expression | None:
        return self._value

    @value.setter
    def value(self, value: Expression) -> None:
        self._value: Expression | None = value

    def c_code(self) -> str:
        if self.value:
            return f"return {self.value.c_code()};"
        else:
            return f"return;"

    def __str__(self) -> str:
        return f"return {self.value.__str__()}"

    def __repr__(self) -> str:
        return f"<ReturnStatement {self.value.__repr__()}>"
