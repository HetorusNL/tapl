#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from contextlib import contextmanager
from typing import Generator
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

        # ensure that we have only the global scope left
        assert len(self._scopes) == 1, f"internal compiler error, more scopes than the global scope left!"

        # if we found errors, print them and exit with exit code 1
        if self._errors:
            [print(e) for e in self._errors]
            exit(1)

    def parse_statement(self, statement: Statement | None) -> None:
        """wrapper around the statement parse to catch exceptions"""
        try:
            if statement:
                self._parse_statement(statement)
        except TaplError as e:
            self._errors.append(e)

    def _parse_statement(self, statement: Statement) -> None:
        # TODO: refactor this to a visitor pattern?
        match statement:
            case AssignmentStatement():
                # check that the identifier exists in the current or outer scopes
                self._ensure_exists(statement.identifier_token)
                # check the value (expression) also for identifiers
                self.parse_expression(statement.value)
            case ExpressionStatement():
                # check the expression also for identifiers
                self.parse_expression(statement.expression)
            case ForLoopStatement():
                # create a new scope for the for loop definition and body statements
                with self._new_scope():
                    # check the statement and expressions that make up the for loop definition
                    self.parse_statement(statement.init)
                    self.parse_expression(statement.check)
                    self.parse_expression(statement.loop)
                    # check all statements inside the body of the for loop
                    for body_statement in statement.statements:
                        self.parse_statement(body_statement)
            case FunctionStatement():
                # create a new scope for the function arguments and body statements
                with self._new_scope():
                    # add the arguments to the newly created scope
                    for type_token, identifier_token in statement.arguments:
                        self._add_identifier(identifier_token, type_token.type_)
                    # check the statements inside the function
                    for body_statement in statement.statements:
                        self.parse_statement(body_statement)
            case IfStatement():
                # create a new scope for the if statement expression and body
                with self._new_scope():
                    # parse the expression and statements
                    self.parse_expression(statement.expression)
                    for body_statement in statement.statements:
                        self.parse_statement(body_statement)
                # loop through all else-if blocks
                for else_if_expression, else_if_statements in statement.else_if_statement_blocks:
                    # create a new scope for the else-if block expression and body
                    with self._new_scope():
                        # parse the expression and statements
                        self.parse_expression(else_if_expression)
                        for else_if_statement in else_if_statements:
                            self.parse_statement(else_if_statement)
                # if there is an else block, loop through its statements
                if else_statements := statement.else_statements:
                    with self._new_scope():
                        for else_statement in else_statements:
                            self.parse_statement(else_statement)
            case PrintStatement():
                # check the expression also for identifiers
                self.parse_expression(statement.value)
            case ReturnStatement():
                # check the return value also for identifiers
                self.parse_expression(statement.value)
            case VarDeclStatement():
                # first check the expression for identifiers
                if initial_value := statement.initial_value:
                    self.parse_expression(initial_value)
                # then add the variable declaration to the scope
                self._add_identifier(statement.name, statement.type_token.type_)
            case _:
                assert False, f"internal compiler error, {type(statement)} not handled!"

    def parse_expression(self, expression: Expression | None) -> None:
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

    @contextmanager
    def _new_scope(self) -> Generator[None]:
        """enter a scope for the content in the 'with' statement"""
        try:
            # first enter the scope by adding a new inner scope to the list
            self._scopes.append({})
            # then give control to the caller
            yield
        finally:
            # no matter if there is an exception, leave the scope
            # remove the innermost scope, making sure that a scope exists
            assert len(self._scopes) > 1, "internal compiler error, trying to leave outermost scope!"
            print(f"leaving {self._scopes[-1]}")
            del self._scopes[-1]

    def ast_error(self, message: str, token: IdentifierToken) -> NoReturn:
        """constructs and raises an AStError"""
        # fill in the filename that we're compiling
        filename: str = str(self._ast.filename.resolve())

        # extract the line number from the token
        line: int = token.line

        # extract the source code line from the file
        source_line: str = Utils.get_source_line(self._ast.filename, line)

        raise AstError(message, filename, line, source_line)
