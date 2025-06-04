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


class TokenExpression(Expression):
    def __init__(self, token: Token):
        super().__init__()
        self._token: Token = token

    @property
    def token(self) -> Token:
        return self._token

    @token.setter
    def token(self, token: Token) -> None:
        self._token: Token = token

    def c_code(self) -> str:
        match self._token.token_type:
            # handle the special cases
            case TokenType.NUMBER:
                assert isinstance(self._token, NumberToken)
                return str(self._token.value)
            case TokenType.STRING:
                assert isinstance(self._token, StringToken)
                return f'"{self._token.value}"'
            case TokenType.IDENTIFIER:
                assert isinstance(self._token, IdentifierToken)
                return self._token.value
            case TokenType.NULL:
                # TODO: refactor to NULL when we support pointers
                return f"0"
            # fall back to the string representation of the token type
            case _:
                return self._token.token_type.value

    def __str__(self) -> str:
        return f"{self._token}"

    def __repr__(self) -> str:
        return f"<TokenExpression {self._token}>"
