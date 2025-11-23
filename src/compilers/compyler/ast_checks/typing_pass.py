#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..errors.tapl_error import TaplError
from ..expressions.binary_expression import BinaryExpression
from ..expressions.call_expression import CallExpression
from ..expressions.expression import Expression
from ..expressions.expression_type import ExpressionType
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
from ..statements.list_statement import ListStatement
from ..statements.print_statement import PrintStatement
from ..statements.return_statement import ReturnStatement
from ..statements.statement import Statement
from ..statements.var_decl_statement import VarDeclStatement
from ..tokens.identifier_token import IdentifierToken
from ..tokens.number_token import NumberToken
from ..tokens.string_token import StringToken
from ..tokens.type_token import TypeToken
from ..tokens.token_type import TokenType
from ..types.class_type import ClassType
from ..types.list_type import ListType
from ..types.numeric_type import NumericType
from ..types.numeric_type_type import NumericTypeType
from ..types.type import Type
from ..types.types import Types
from ..utils.ast import AST
from ..utils.source_location import SourceLocation


class TypingPass(PassBase):
    def __init__(self, ast: AST):
        super().__init__(ast)
        # extract the types as determined during the type resolving pass
        self._types: Types = ast.types
        # store a list of functions
        # TODO: functions should be callable from everywhere
        self._functions: dict[str, FunctionStatement] = {}
        # TODO: classes should be usable from everywhere
        self._classes: dict[str, ClassStatement] = {}
        # store a stack of class types of variables
        self._classes_stack: list[Type] = []
        # store a stack of function return types
        self._function_stack: list[Type] = []
        # store a stack of identifier types when they have inner identifiers
        self._identifier_stack: list[Type] = []

    def _parse_statement(self, statement: Statement) -> None:
        # TODO: refactor this and _parse_expression to a visitor pattern?
        match statement:
            case AssignmentStatement():
                # get the identifier token type
                requested_type: Type = self.parse_expression(statement.expression)
                # check that the expression is of this type
                value_type: Type = self.parse_expression(statement.value)
                # check that returned type and requested are valid
                self._check_types(requested_type, value_type, statement.value.source_location)
            case ClassStatement():
                # TODO: implement
                self._classes[statement.class_type.keyword] = statement
            case ExpressionStatement():
                # check the expression
                self.parse_expression(statement.expression)
            case ForLoopStatement():
                # create a new scope for the for loop definition and body statements
                with self._new_scope():
                    # check the statement and expressions that make up the for loop definition
                    self.parse_statement(statement.init)
                    if statement.check:
                        self.parse_expression(statement.check)
                    if statement.loop:
                        self.parse_expression(statement.loop)
                    # check all statements inside the body of the for loop
                    for body_statement in statement.statements:
                        self.parse_statement(body_statement)
            case FunctionStatement():
                # add the function name to the surrounding scope
                self._add_identifier(statement.name, statement.return_type.type_)
                # add the function to the function list
                self._functions[statement.name.value] = statement
                # create a new scope for the function arguments and body statements
                with self._new_scope():
                    # add the return type to the function return type stack
                    self._function_stack.append(statement.return_type.type_)
                    try:
                        # add the arguments to the newly created scope
                        for type_token, identifier_token in statement.arguments:
                            self._add_identifier(identifier_token, type_token.type_)
                        # check the statements inside the function
                        for body_statement in statement.statements:
                            self.parse_statement(body_statement)
                    finally:
                        self._function_stack.pop()
            case IfStatement():
                # pretty nice, this parsing is the same as the scoping pass :)
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
            case ListStatement():
                # add the variable declaration to the scope
                self._add_identifier(statement.name, statement.list_type)
            case PrintStatement():
                # check the expression
                self.parse_expression(statement.value)
            case ReturnStatement():
                # we only need to type check the return statement, the rest is already done at this point
                function_return_type: Type = self._function_stack[-1]
                non_void: bool = function_return_type.non_void()
                if non_void and not statement.value:
                    # if non_void, we need a return value
                    self.ast_error(f"non-void function expects a return value!", statement.source_location)
                if not non_void and statement.value:
                    # if void, we don't want a return value
                    message: str = f"void function expects no return value, found '{statement.value}'!"
                    source_location: SourceLocation = statement.value.source_location
                    self.ast_error(message, source_location)
                if statement.value:
                    return_value_type: Type = self.parse_expression(statement.value)
                    source_location: SourceLocation = statement.value.source_location
                    try:
                        # perform type checking on the requested return type and provided return value,
                        # and catch an exception if it occurs
                        self._check_types(function_return_type, return_value_type, source_location)
                    except TaplError:
                        # the type check failed, formulate a nice error for the user
                        message: str = f"expected return value of type '{function_return_type.keyword}', "
                        message += f"but found '{return_value_type.keyword}'!"
                        self.ast_error(message, source_location)
            case VarDeclStatement():
                # add the variable declaration to the scope (we may need it already when testing the initial value)
                self._add_identifier(statement.name, statement.type_token.type_)
                # get the type of the initial value
                if initial_value := statement.initial_value:
                    # get the identifier token type
                    requested_type: Type = self._get_type(statement.name)
                    # check that the expression is of this type
                    value_type: Type = self.parse_expression(initial_value)
                    # check that returned type and requested are valid
                    self._check_types(requested_type, value_type, initial_value.source_location)
            case _:
                assert False, f"internal compiler error, {type(statement)} not handled!"

    def parse_expression(self, expression: Expression) -> Type:
        """parse an expression, where exceptions are thrown toward the surrounding statement"""
        # parse all types of expressions
        match expression:
            case BinaryExpression():
                # check the left and right expression of the binary expression
                type_left: Type = self.parse_expression(expression.left)
                type_right: Type = self.parse_expression(expression.right)
                return self._check_types(type_left, type_right, expression.source_location)
            case CallExpression():
                # assert that we don't have an inner expression in the identifier expression
                assert expression.expression.inner_expression is None
                identifier_token: IdentifierToken = expression.expression.identifier_token
                # check that the expression is callable
                if function := self._functions.get(identifier_token.value):
                    # check that the amount of arguments are correct
                    required_arguments: int = len(function.arguments)
                    passed_arguments: int = len(expression.arguments)
                    if len(function.arguments) != len(expression.arguments):
                        message: str = f"'{identifier_token}' expected {required_arguments} argument(s), "
                        message += f"but {passed_arguments} were passed!"
                        self.ast_error(message, expression.source_location)
                    # for all arguments, check the types
                    for arg_index in range(required_arguments):
                        # get the type of the required argument
                        required_argument_type_token: TypeToken = function.arguments[arg_index][0]
                        required_argument_type: Type = required_argument_type_token.type_
                        # get the type of the passed argument
                        passed_argument: Expression = expression.arguments[arg_index]
                        passed_argument_type: Type = self.parse_expression(passed_argument)
                        source_location: SourceLocation = passed_argument.source_location
                        # check that the types are correct
                        try:
                            # perform the type check, and catch an exception if it occurs
                            self._check_types(required_argument_type, passed_argument_type, source_location)
                        except TaplError:
                            # the type check failed, formulate a nice error for the user
                            message: str = f"expected 'argument {arg_index+1}' of type "
                            message += f"'{required_argument_type.keyword}', "
                            message += f"but found '{passed_argument_type.keyword}'!"
                            self.ast_error(message, source_location)
                    # return the return type of the function
                    return self._get_type(identifier_token)
                elif self._classes_stack:
                    # TODO: implement
                    # return classes[class][function].type
                    expression.class_type = self._classes[self._classes_stack[-1].keyword].class_type
                    return Type("u32")  # self._get_type(identifier_token)
                elif self._identifier_stack:
                    # if there is a list on the identifier stack, we can call certain functions
                    type_: Type = self._identifier_stack[-1]
                    if isinstance(type_, ListType):
                        if identifier_token.value in type_.callable_functions():
                            return type_
                        # otherwise it's not callable, add the error
                        source_location: SourceLocation = identifier_token.source_location
                        self.ast_error(
                            f"identifier '{identifier_token}' of a '{type_}' is not callable!", source_location
                        )
                source_location: SourceLocation = identifier_token.source_location
                self.ast_error(f"identifier '{identifier_token}' is not callable!", source_location)
            case IdentifierExpression():
                # TODO: implement
                with self._new_scope():
                    type_: Type = self._get_type(expression.identifier_token)
                    is_class: bool = isinstance(type_, ClassType)
                    if is_class:
                        self._classes_stack.append(type_)
                        expression.class_type = self._classes[type_.keyword].class_type
                    self._identifier_stack.append(type_)
                    if isinstance(type_, ListType):
                        expression.list_type = type_
                    try:
                        if expression.inner_expression:
                            return self.parse_expression(expression.inner_expression)
                    finally:
                        self._identifier_stack.pop()
                        if is_class:
                            self._classes_stack.pop()
                return self._get_type(expression.identifier_token)
            case TokenExpression():
                match expression.token:
                    case NumberToken():
                        # no checking happens here so we're going to return a base type
                        return self._types["base"]
                    case StringToken():
                        return self._types["string"]
                    case IdentifierToken():
                        # TODO: handle callables differently, this now results in gcc errors
                        # get the type from the identifier
                        return self._get_type(expression.token)
                    case _:
                        match expression.token.token_type:
                            # TODO: refactor true/false to special booleans
                            case TokenType.TRUE:
                                return self._types["base"]
                            case TokenType.FALSE:
                                return self._types["base"]
                            case TokenType.NULL:
                                # TODO: refactor when ptr implemented
                                return self._types["base"]
                            case _:
                                assert False, "TODO: process generic token thing"
            case TypeCastExpression():
                # get the type of the inner expression
                inner_type = self.parse_expression(expression.expression)
                cast_to_type: Type = expression.cast_to.type_
                # we allow any NumericType to be type casted, otherwise we fail
                if isinstance(cast_to_type, NumericType) and isinstance(inner_type, NumericType):
                    return cast_to_type
                else:
                    message: str = f"cannot type cast from '{inner_type.keyword}' to '{cast_to_type.keyword}'!"
                    self.ast_error(message, expression.source_location)
            case UnaryExpression():
                inner_type: Type = self.parse_expression(expression.expression)
                if expression.expression_type == ExpressionType.GROUPING:
                    # if it's a grouping, anything goes, return the inner type
                    return inner_type
                else:
                    # otherwise it must be a numeric type
                    if not isinstance(inner_type, NumericType):
                        message: str = f"expected numeric type for unary expression '{expression.expression_type.name}'"
                        message += f", found '{inner_type.keyword}'!"
                        self.ast_error(message, expression.expression.source_location)
                    return inner_type
            case _:
                assert False, f"internal compiler error, {type(expression)} not handled!"

    def _check_identifier(self, identifier_token: IdentifierToken, target_type: Type) -> None:
        identifier_type: Type = self._get_type(identifier_token)
        if identifier_type != target_type:
            message: str = f"identifier {identifier_token.value} is of type {identifier_type.keyword}, "
            message += f"cannot assign value of type {target_type.keyword}!"
            self.ast_error(message, identifier_token.source_location)

    def _get_type(self, identifier_token: IdentifierToken) -> Type:
        """checks that the type of the identifier_token matches the type provided"""
        identifier: str = identifier_token.value
        # go through the scopes in reverse order, and get the type
        for scope in reversed(self._scopes):
            if identifier_type := scope.get(identifier):
                return identifier_type
        assert False, f"internal compiler error, {identifier} not found in scopes!"

    def _check_types(self, left: Type, right: Type, source_location: SourceLocation) -> Type:
        # TODO: we should check the size of a base type if the other side is no base type with _check_number_token(...)
        # check if they are both number types
        if isinstance(left, NumericType) and isinstance(right, NumericType):
            # check if there are two base types
            if left.keyword == "base" and right.keyword == "base":
                # return the base type as type
                return left
            if left.keyword == "base":
                # return the right side, as left is a base type
                return right
            if right.keyword == "base":
                # return the left side, as right is a base type
                return left

        # if both sides are not NumericType, the types must match exactly
        if left.keyword == right.keyword:
            return left

        # TODO: allow for a custom error message in this function
        # otherwise we have conflicting types, generate an error
        message: str = f"invalid types provided, '{left.keyword}' and '{right.keyword}' can't be used together!"
        self.ast_error(message, source_location)

    def _check_number_token(self, requested_type: Type, expression: TokenExpression) -> Type:
        # TODO: add num bits to the token itself, instead of calculating it here

        # type sanity checks
        assert type(requested_type) == NumericType
        assert type(expression.token) == NumberToken

        # check the value of the provided NumberToken and the requested type
        match requested_type.numeric_type_type:
            case NumericTypeType.SIGNED:
                # TODO: this will overflow in the non-python compiler
                max_value: int = 2 ** (requested_type.num_bits - 1) - 1  # 0x7F~ -> 127~
                min_value: int = -max_value - 1  # 0x80~ -> -128~
            case NumericTypeType.UNSIGNED:
                # TODO: this will overflow in the non-python compiler
                max_value: int = 2 ** (requested_type.num_bits) - 1  # 0xFF~ -> 255~
                min_value: int = 0  # 0x00~ -> 0
            case NumericTypeType.FLOATING_POINT:
                # nothing to check here
                return requested_type

        # signed/unsigned numbers must fit the num_bits
        value: int = expression.token.value
        if value < min_value or value > max_value:
            message: str = f"can't assign '{value}' to '{requested_type.keyword}', "
            message += f"value must be between [{min_value}, {max_value}]!"
            self.ast_error(message, expression.source_location)

        # all checks passed, return the requested type
        return requested_type
