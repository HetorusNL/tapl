#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from ..expressions.identifier_expression import IdentifierExpression
from ..tokens.type_token import TypeToken
from ..utils.source_location import SourceLocation


class CallExpression(Expression):
    def __init__(
        self,
        source_location: SourceLocation,
        expression: IdentifierExpression,
        class_name: TypeToken | None,
        arguments: list[Expression] = [],
    ):
        super().__init__(source_location)
        self.expression: IdentifierExpression = expression
        self.class_name: TypeToken | None = class_name
        self.arguments: list[Expression] = arguments

    def c_code(self) -> str:
        # build the argument list
        arguments: list[str] = []
        # if it's a class method call, prepend the 'this' argument
        if self.class_name:
            arguments.append("this")
        for argument in self.arguments:
            arguments.append(argument.c_code())
        arguments_string: str = ", ".join(arguments)

        # construct the function name
        function_name: str = f"{self.expression.c_code()}"
        # if it's a class method call, prepend the class name
        if self.class_name:
            function_name = f"{self.class_name}_{function_name}"

        # construct and return the whole function call
        return f"{function_name}({arguments_string})"

    def __str__(self) -> str:
        return f'{self.expression.__str__()}({", ".join([argument.__str__() for argument in self.arguments])})'

    def __repr__(self) -> str:
        return f"<CallExpression: location {self.source_location}, {self.expression.__repr__()}>"
