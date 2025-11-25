#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .expression import Expression
from ..tokens.string_chars_token import StringCharsToken
from ..tokens.token import Token
from ..tokens.token_type import TokenType
from ..utils.source_location import SourceLocation


class StringExpression(Expression):
    def __init__(self, string_start: Token):
        source_location: SourceLocation = string_start.source_location
        super().__init__(source_location)
        self.string_elements: list[Token | Expression] = [string_start]

    def add_token(self, element: Token | Expression) -> None:
        self.source_location += element.source_location
        self.string_elements.append(element)

    def _raw_string(self) -> str:
        string: str = ""
        for element in self.string_elements:
            # check if the element is an expression, if so add its c_code
            if isinstance(element, Expression):
                string += element.c_code()
                continue
            # otherwise it's a string-related token, process it
            token: Token = element
            match token.token_type:
                case TokenType.STRING_START:
                    string += '"'
                case TokenType.STRING_END:
                    string += '"'
                case TokenType.STRING_CHARS:
                    assert isinstance(token, StringCharsToken)
                    string += token.value
                case TokenType.STRING_EXPR_START:
                    string += "{"
                case TokenType.STRING_EXPR_END:
                    string += "}"
                case _:
                    assert False
        return string

    def c_code(self) -> str:
        # TODO: implement
        return self._raw_string()

    def __str__(self) -> str:
        return self._raw_string()

    def __repr__(self) -> str:
        return f"<StringExpression: location {self.source_location}, {self._raw_string()}"
