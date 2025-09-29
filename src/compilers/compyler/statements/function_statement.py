#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .statement import Statement
from ..tokens.identifier_token import IdentifierToken
from ..tokens.type_token import TypeToken
from ..utils.source_location import SourceLocation


class FunctionStatement(Statement):
    def __init__(self, return_type: TypeToken, name: IdentifierToken):
        # store the initial source location, where arguments are added later
        source_location: SourceLocation = return_type.source_location + name.source_location
        super().__init__(source_location)
        self.return_type: TypeToken = return_type
        self.name: IdentifierToken = name
        self.arguments: list[tuple[TypeToken, IdentifierToken]] = []
        self.statements: list[Statement] = []

    def add_argument(self, argument_type: TypeToken, argument_name: IdentifierToken) -> None:
        # add the source lcoation of the argument type and name
        self.source_location += argument_type.source_location + argument_name.source_location
        # add the argument to the class
        self.arguments.append((argument_type, argument_name))

    def _c_declaration_base(self) -> str:
        """returns the function declaration line, without anything after the closing paren"""
        # start with the function return type and name
        code: str = f"{self.return_type.type_.keyword} {self.name.value}("

        # create a list of argument type-name pairs
        arguments: list[str] = []
        for argument_type, argument_name in self.arguments:
            arguments.append(f"{argument_type.type_.keyword} {argument_name.value}")
        # add comma separated list of the argument type-name pairs
        code += ", ".join(arguments)
        code += f")"

        return code

    def c_declaration(self) -> str:
        """returns the function declaration with terminating semicolon"""
        code: str = f"{self._c_declaration_base()};"

        return code

    def c_code(self) -> str:
        """returns declaration and body of the function"""
        code: str = f"{self._c_declaration_base()} {{\n"

        # add the statements if they exist
        for statement in self.statements:
            code += f"{statement.c_code()}\n"

        # end with the closing bracket
        code += f"}}"

        return code

    def __str__(self) -> str:
        return f"{self.return_type.type_.keyword} {self.name.value}: ..."

    def __repr__(self) -> str:
        string: str = f"<FunctionStatement, location {self.source_location},"
        string += f" {self.return_type.type_.keyword} {self.name.value}>"
        return string
