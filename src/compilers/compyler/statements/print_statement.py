#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from ..expressions.token_expression import TokenExpression
from .statement import Statement
from ..tokens.token import Token
from ..tokens.token_type import TokenType
from ..utils.source_location import SourceLocation


class PrintStatement(Statement):
    def __init__(self, token: Token, value: Expression):
        source_location: SourceLocation = token.source_location + value.source_location
        super().__init__(source_location)
        self.value: Expression = value

    def c_code(self) -> str:
        expression: str = self.value.c_code()

        # check if the value is a string
        if isinstance(self.value, TokenExpression):
            if self.value.token.token_type == TokenType.STRING:
                # printn the token as string
                return f'printf("%s\\n", {expression});'

        # otherwise we fall back to a signed integer
        return f'printf("%d\\n", {expression});'

    def __str__(self) -> str:
        return f"print({self.value.__str__()})"

    def __repr__(self) -> str:
        return f"<PrintStatement: location {self.source_location}, {self.value.__repr__()}>"
