#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .expression import Expression
from ..tokens.identifier_token import IdentifierToken
from ..tokens.number_token import NumberToken
from ..tokens.string_token import StringToken
from ..tokens.token import Token
from ..tokens.token_type import TokenType
from ..utils.source_location import SourceLocation


class TokenExpression(Expression):
    def __init__(self, source_location: SourceLocation, token: Token):
        super().__init__(source_location)
        self.token: Token = token

    def c_code(self) -> str:
        match self.token.token_type:
            # handle the special cases
            case TokenType.NUMBER:
                assert isinstance(self.token, NumberToken)
                return str(self.token.value)
            case TokenType.STRING_CHARS:
                assert isinstance(self.token, StringToken)
                return f'"{self.token.value}"'
            case TokenType.IDENTIFIER:
                assert isinstance(self.token, IdentifierToken)
                return self.token.value
            case TokenType.NULL:
                # TODO: refactor to NULL when we support pointers
                return f"0"
            # fall back to the string representation of the token type
            case _:
                return self.token.token_type.value

    def __str__(self) -> str:
        return f"{self.token}"

    def __repr__(self) -> str:
        return f"<TokenExpression: location {self.source_location}, {self.token}>"
