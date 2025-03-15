#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .statement import Statement
from ..tokens.identifier_token import IdentifierToken


class IdentifierStatement(Statement):
    def __init__(self, identifier_token: IdentifierToken):
        super().__init__()
        self._identifier_token: IdentifierToken = identifier_token

    @property
    def identifier_token(self) -> IdentifierToken:
        return self._identifier_token

    @identifier_token.setter
    def identifier_token(self, identifier_token: IdentifierToken) -> None:
        self._identifier_token: IdentifierToken = identifier_token

    def c_code(self) -> str:
        identifier: str = self.identifier_token.value

        return f"{identifier};"
