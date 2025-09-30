#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.


from contextlib import contextmanager
from typing import Generator
from typing import NoReturn

from ..errors.ast_error import AstError
from ..errors.tapl_error import TaplError
from ..statements.statement import Statement
from ..tokens.identifier_token import IdentifierToken
from ..types.type import Type
from ..utils.ast import AST
from ..utils.source_location import SourceLocation


class PassBase:
    """Base class of AST check passes, with the common functionality"""

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
        """wrapper around the statement parsing to catch and handle exceptions"""
        try:
            if statement:
                self._parse_statement(statement)
        except TaplError as e:
            self._errors.append(e)

    def _parse_statement(self, statement: Statement) -> None:
        raise NotImplementedError()

    def _add_identifier(self, identifier_token: IdentifierToken, type_: Type):
        """first checks if the identifier already exists in innermost scope, otherwise adds identifier"""
        identifier: str = identifier_token.value
        # check in the innermost scope if the identifier already exists
        if identifier in self._scopes[-1]:
            self.ast_error(f"identifier '{identifier}' already exists!", identifier_token.source_location)

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
            print(f"leaving scope with identifiers: {{{', '.join(self._scopes[-1].keys())}}}")
            del self._scopes[-1]

    def ast_error(self, message: str, source_location: SourceLocation) -> NoReturn:
        """constructs and raises an AStError"""
        raise AstError(message, self._ast.filename, source_location)
