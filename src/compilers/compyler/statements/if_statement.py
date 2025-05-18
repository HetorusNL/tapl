#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement


class IfStatement(Statement):
    def __init__(self, expression: Expression, statements: list[Statement]):
        super().__init__()
        self._expression: Expression = expression
        self._statements: list[Statement] = statements
        self._else_if_statement_blocks: list[tuple[Expression, list[Statement]]] = []
        self._else_statements: list[Statement] | None = None

    @property
    def expression(self) -> Expression:
        return self._expression

    @expression.setter
    def expression(self, expression: Expression) -> None:
        self._expression: Expression = expression

    @property
    def statements(self) -> list[Statement]:
        return self._statements

    @statements.setter
    def statements(self, statements: list[Statement]) -> None:
        self._statements: list[Statement] = statements

    @property
    def else_if_statement_blocks(self) -> list[tuple[Expression, list[Statement]]]:
        return self._else_if_statement_blocks

    def add_else_if_statement_block(self, expression: Expression, statement_block: list[Statement]) -> None:
        self._else_if_statement_blocks.append((expression, statement_block))

    @property
    def else_statements(self) -> list[Statement] | None:
        return self._else_statements

    @else_statements.setter
    def else_statements(self, statements: list[Statement]) -> None:
        self._else_statements: list[Statement] | None = statements

    def add_if_statement(self, code: str | None, expression: Expression, statements: list[Statement]) -> str:
        # add the expression in the if statement
        new_code: str = f"if ({expression.c_code()}) {{\n"
        # add the statements of the if block
        for statement in statements:
            new_code += f"{statement.c_code()}\n"
        # end with the closing brace
        new_code += f"}}"

        if code:
            # append the statement to an already existing code string
            return code + new_code
        # otherwise return the newly created code
        return new_code

    def c_code(self) -> str:
        # construct the if statement
        code: str = self.add_if_statement(None, self.expression, self.statements)

        # add the else if blocks if they exist
        for else_expression, statements in self.else_if_statement_blocks:
            # add the else line
            code += f" else "
            # add the else-if statement
            code: str = self.add_if_statement(code, else_expression, statements)

        # add the else block if it exists
        if self.else_statements is not None:
            # add the else line
            code += f" else {{\n"
            for statement in self.else_statements:
                code += f"{statement.c_code()}\n"
            # end with the closing brace
            code += f"}}"

        return code

    def __str__(self) -> str:
        return f"if ({self.expression.__str__()}): ..."

    def __repr__(self) -> str:
        return f"<IfStatement {self.expression.__repr__()}>"
