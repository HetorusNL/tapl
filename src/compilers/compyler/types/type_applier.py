#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..tokens.identifier_token import IdentifierToken
from ..tokens.token import Token
from ..tokens.var_decl_token import VarDeclToken
from .types import Types
from ..utils.stream import Stream


class TypeApplier:
    def __init__(self, types: Types):
        self._types: Types = types

    def apply(self, tokens: Stream[Token]) -> Stream[Token]:
        """loop through the provided token stream.
        replace the type token and variable name token with a single variable declaration token.
        modifies the token stream inplace, and returns a reference to the stream.
        """

        # find type and identifier tokens of a variable declaration
        # consume those two and add a var_decl token
        # loop through the tokens to find variable declarations
        for token in tokens.iter():
            if isinstance(token, IdentifierToken):
                # check that the identifier corresponds with a type
                if var_type := self._types.get(token.value):
                    # get the next token, should be the variable name
                    next_token: Token = tokens.iter_next()
                    if isinstance(next_token, IdentifierToken):
                        # found the variable name, construct the var_decl token
                        line: int = token.line
                        name: str = next_token.value
                        var_decl: VarDeclToken = VarDeclToken(line, var_type, name)
                        # replace the type and variable name token with var_decl
                        tokens.replace(2, var_decl)

        return tokens
