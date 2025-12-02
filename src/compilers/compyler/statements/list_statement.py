#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .statement import Statement
from ..tokens.identifier_token import IdentifierToken
from ..tokens.token import Token
from ..types.list_type import ListType
from ..utils.source_location import SourceLocation


class ListStatement(Statement):
    def __init__(self, list_token: Token, list_type: ListType, name: IdentifierToken):
        # formulate the source location from the list statement from list till name
        source_location: SourceLocation = list_token.source_location + name.source_location
        super().__init__(source_location)

        # store the rest of the variables in the class
        self.list_type: ListType = list_type
        self.name: IdentifierToken = name

    def c_code(self) -> str:
        # create the list declaration
        code: str = f"list_{self.list_type.inner_type} {self.name};"
        # also initialize the list to zero
        code += f"{self.name}.list = 0;"
        return code

    def __str__(self) -> str:
        return f"{self.list_type.keyword} {self.name}"

    def __repr__(self) -> str:
        return f"<ListStatement: location {self.source_location}, {self.list_type.keyword} {self.name}"
