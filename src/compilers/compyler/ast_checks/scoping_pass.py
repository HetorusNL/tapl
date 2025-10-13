#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..errors.tapl_error import TaplError
from ..expressions.binary_expression import BinaryExpression
from ..expressions.call_expression import CallExpression
from ..expressions.expression import Expression
from ..expressions.identifier_expression import IdentifierExpression
from ..expressions.token_expression import TokenExpression
from ..expressions.type_cast_expression import TypeCastExpression
from ..expressions.unary_expression import UnaryExpression
from .pass_base import PassBase
from ..statements.assignment_statement import AssignmentStatement
from ..statements.class_statement import ClassStatement
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


class ScopingPass(PassBase):
    def __init__(self, ast: AST):
        super().__init__(ast)

    def _parse_statement(self, statement: Statement) -> None:
        # TODO: refactor this and _parse_expression to a visitor pattern?
        match statement:
            case AssignmentStatement():
                # check that the this or identifier expression
                self.parse_expression(statement.expression)
                # check the value (expression) also for identifiers
                self.parse_expression(statement.value)
            case ClassStatement():
                # TODO: implement
                pass
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
                # add the function name to the surrounding scope
                self._add_identifier(statement.name, statement.return_type.type_)
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
        """wrapper around the expression parsing to catch and handle exceptions"""
        try:
            if expression:
                self._parse_expression(expression)
        except TaplError as e:
            self._errors.append(e)

    def _parse_expression(self, expression: Expression) -> None:
        match expression:
            case BinaryExpression():
                # check the left and right expression of the binary expression
                self.parse_expression(expression.left)
                self.parse_expression(expression.right)
            case CallExpression():
                # check that the function name (possibly nested expressions) exists
                self.parse_expression(expression.expression)
                # check all argument expressions
                for argument in expression.arguments:
                    self.parse_expression(argument)
            case IdentifierExpression():
                # TODO: implement
                pass
            case TokenExpression():
                # check if it is a token expression
                if type(expression.token) == IdentifierToken:
                    # check that the identifier exists in the current or outer scopes
                    self._ensure_exists(expression.token)
            case TypeCastExpression():
                # check the expression being type-casted
                self.parse_expression(expression.expression)
            case UnaryExpression():
                # check the expression within the unary expression
                self.parse_expression(expression.expression)
            case _:
                assert False, f"internal compiler error, {type(expression)} not handled!"

    def _ensure_exists(self, identifier_token: IdentifierToken) -> Type:
        """checks that the identifier exists in current or outer scopes, and return its type"""
        identifier: str = identifier_token.value
        # go through the scopes in reverse order, and return the type if it exists
        for scope in reversed(self._scopes):
            if identifier_type := scope.get(identifier):
                return identifier_type

        # the identifier doesn't exist, raise an error
        self.ast_error(f"unknown identifier '{identifier}'!", identifier_token.source_location)
