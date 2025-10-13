#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from ..expressions.identifier_expression import IdentifierExpression
from ..expressions.this_expression import ThisExpression
from .statement import Statement
from ..utils.source_location import SourceLocation


class AssignmentStatement(Statement):
    def __init__(self, expression: ThisExpression | IdentifierExpression, value: Expression):
        source_location: SourceLocation = expression.source_location + value.source_location
        super().__init__(source_location)
        self.expression: ThisExpression | IdentifierExpression = expression
        self.value: Expression = value

    def c_code(self) -> str:
        identifier: str = self.expression.c_code()
        value: str = self.value.c_code()

        return f"{identifier} = {value};"

    def __str__(self) -> str:
        identifier: str = self.expression.__str__()
        value: str = self.value.__str__()

        return f"{identifier} = {value}"

    def __repr__(self) -> str:
        identifier: str = self.expression.__repr__()
        value: str = self.value.__repr__()

        return f"<AssignmantStatement: location {self.source_location}, {identifier} = {value}>"
