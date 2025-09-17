#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .token_type import TokenType
from .token import Token
from ..utils.source_location import SourceLocation


class NumberToken(Token):
    def __init__(self, source_location: SourceLocation, value: int):
        super().__init__(TokenType.NUMBER, source_location)
        # store the additional properties in the class
        self.value: int = value

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"<{self.token_type}: location {self.source_location}, {self.value}>"
