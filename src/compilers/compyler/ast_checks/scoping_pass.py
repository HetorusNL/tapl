#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from typing import NoReturn

from ..errors.tapl_error import TaplError
from ..errors.ast_error import AstError
from ..expressions.expression import Expression
from ..statements.assignment_statement import AssignmentStatement
from ..statements.expression_statement import ExpressionStatement
from ..statements.for_loop_statement import ForLoopStatement
from ..statements.function_statement import FunctionStatement
from ..statements.if_statement import IfStatement
from ..statements.print_statement import PrintStatement
from ..statements.return_statement import ReturnStatement
from ..statements.statement import Statement
from ..statements.var_decl_statement import VarDeclStatement
from ..tokens.identifier_token import IdentifierToken
from ..types.type import Type
from ..utils.ast import AST
from ..utils.utils import Utils


class ScopingPass:
    def __init__(self, ast: AST):
        self._ast: AST = ast
        # store a list of scopes that stores the variable name and its type
        # pre-populate the scopes list with the (empty) outer scope
        self._scopes: list[dict[str, Type]] = [{}]
        # store a list of errors during this pass, if they occur
        self._errors: list[TaplError] = []

    def run(self) -> None:
        for statement in self._ast.statements.iter():
            self.parse_statement(statement)

        # if we found errors, print them and exit with exit code 1
        if self._errors:
            [print(e) for e in self._errors]
            exit(1)

    def parse_statement(self, statement: Statement) -> None:
        """wrapper around the statement parse to catch exceptions"""
        try:
            self._parse_statement(statement)
        except TaplError as e:
            self._errors.append(e)

    def _parse_statement(self, statement: Statement) -> None:
        match statement:
            case AssignmentStatement():
                # check that the identifier exists in the current or outer scopes
                self._ensure_exists(statement.identifier_token)
                # check the value (expression) also for identifiers
                self._parse_expression(statement.value)
            case ExpressionStatement():
                # check the expression also for identifiers
                self._parse_expression(statement.expression)
            case ForLoopStatement():
                pass  # TODO: implement
            case FunctionStatement():
                pass  # TODO: implement with scopes and such
                # check the statements inside the function
                for s in statement.statements:
                    self.parse_statement(s)
            case IfStatement():
                pass  # TODO: implement
            case PrintStatement():
                pass  # TODO: implement
            case ReturnStatement():
                pass  # TODO: implement
            case VarDeclStatement():
                name: str = statement.name.value
                type_: Type = statement.type_token.type_
                initial_value: Expression | None = statement.initial_value
                # first check the expression for identifiers
                if initial_value:
                    self._parse_expression(initial_value)
                # then add the variable declaration to the scope
                self._scopes[-1][name] = type_
            case _:
                pass
                assert False, f"internal compiler error, {type(statement)} not handled!"

    def _parse_expression(self, expression: Expression) -> None:
        # TODO: check expressions also
        pass

    def _ensure_exists(self, identifier_token: IdentifierToken) -> Type:
        """checks that the identifier exists in current or outer scopes, and return its type"""
        identifier: str = identifier_token.value
        # go through the scopes in reverse order, and return the type if it exists
        for scope in reversed(self._scopes):
            if identifier_type := scope.get(identifier):
                return identifier_type

        # the identifier doesn't exist, raise an error
        self.ast_error(f"unknown identifier '{identifier}'!", identifier_token)

    def _add_identifier(self, identifier_token: IdentifierToken, type_: Type):
        """first checks if the identifier already exists in innermost scope, otherwise adds identifier"""
        identifier: str = identifier_token.value
        # check in the innermost scope if the identifier already exists
        if identifier in self._scopes[-1]:
            self.ast_error(f"identifier '{identifier}' already exists!", identifier_token)

        # otherwise add the identifier in the innermost scope
        self._scopes[-1][identifier] = type_

    def ast_error(self, message: str, token: IdentifierToken) -> NoReturn:
        """constructs and raises an AStError"""
        # fill in the filename that we're compiling
        filename: str = str(self._ast.filename.resolve())

        # extract the line number from the token
        line: int = token.line

        # extract the source code line from the file
        source_line: str = Utils.get_source_line(self._ast.filename, line)

        raise AstError(message, filename, line, source_line)
