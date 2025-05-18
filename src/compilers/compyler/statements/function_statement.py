#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .statement import Statement
from ..tokens.identifier_token import IdentifierToken
from ..tokens.type_token import TypeToken


class FunctionStatement(Statement):
    def __init__(self, return_type: TypeToken, name: IdentifierToken):
        super().__init__()
        self._return_type: TypeToken = return_type
        self._name: IdentifierToken = name
        self._arguments: list[tuple[TypeToken, IdentifierToken]] = []
        self._statements: list[Statement] = []

    @property
    def return_type(self) -> TypeToken:
        return self._return_type

    @return_type.setter
    def return_type(self, return_type: TypeToken) -> None:
        self._return_type: TypeToken = return_type

    @property
    def name(self) -> IdentifierToken:
        return self._name

    @name.setter
    def name(self, name: IdentifierToken) -> None:
        self._name: IdentifierToken = name

    @property
    def arguments(self) -> list[tuple[TypeToken, IdentifierToken]]:
        return self._arguments

    def add_argument(self, argument_type: TypeToken, argument_name: IdentifierToken) -> None:
        self._arguments.append((argument_type, argument_name))

    @property
    def statements(self) -> list[Statement]:
        return self._statements

    @statements.setter
    def statements(self, statements: list[Statement]) -> None:
        self._statements: list[Statement] = statements

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
        return f"<FunctionStatement {self.return_type.type_.keyword} {self.name.value}>"
