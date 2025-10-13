#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .expression import Expression
from ..utils.source_location import SourceLocation


class ThisExpression(Expression):
    def __init__(self, source_location: SourceLocation, inner_expression: Expression):
        super().__init__(source_location)
        self.inner_expression: Expression = inner_expression

    def __str__(self) -> str:
        return f"this.{self.inner_expression}"

    def __repr__(self) -> str:
        return f"<ThisExpression: location {self.source_location}, this.{self.inner_expression}>"
