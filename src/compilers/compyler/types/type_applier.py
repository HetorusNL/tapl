#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..tokens.identifier_token import IdentifierToken
from ..tokens.token import Token
from ..tokens.type_token import TypeToken
from .types import Types
from ..utils.stream import Stream


class TypeApplier:
    def __init__(self, types: Types):
        self._types: Types = types

    def apply(self, tokens: Stream[Token]) -> Stream[Token]:
        """loop through the provided token stream.
        replace the IdentifierToken that is a type with a TypeToken.
        modifies the token stream inplace, and returns a reference to the stream.
        """

        # find a type IdentifierToken
        # consume the token and add a TypeToken
        # loop through the tokens to find the types
        for token in tokens.iter():
            if isinstance(token, IdentifierToken):
                # check that the identifier corresponds with a type
                if var_type := self._types.get(token.value):
                    # found the type of the IdentifierToken, construct the TypeToken
                    line: int = token.line
                    type_token: TypeToken = TypeToken(line, var_type)
                    # replace the IdentifierToken with a TypeToken
                    tokens.replace(1, type_token)

        return tokens
