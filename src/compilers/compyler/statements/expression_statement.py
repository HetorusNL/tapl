#!/usr/bin/env python
#
# Copyright (c) 2026 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement
from ..utils.source_location import SourceLocation


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        source_location: SourceLocation = expression.source_location
        super().__init__(source_location)
        self.expression: Expression = expression

    def c_code(self) -> str:
        expression_code: str = self.expression.c_code()

        return f"{expression_code};"

    def __str__(self) -> str:
        return self.expression.__str__()

    def __repr__(self) -> str:
        return f"<ExpressionStatement: location {self.source_location}, {self.expression.__repr__()}>"
