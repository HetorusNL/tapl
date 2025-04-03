#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .errors.ast_error import AstError
from .expressions.binary_expression import BinaryExpression
from .expressions.expression import Expression
from .expressions.unary_expression import UnaryExpression
from .expressions.token_expression import TokenExpression
from .expressions.expression_type import ExpressionType
from .statements.assignment_statement import AssignmentStatement
from .statements.expression_statement import ExpressionStatement
from .statements.identifier_statement import IdentifierStatement
from .statements.print_statement import PrintStatement
from .statements.statement import Statement
from .statements.var_decl_statemtnt import VarDeclStatement
from .tokens.identifier_token import IdentifierToken
from .tokens.token import Token
from .tokens.var_decl_token import VarDeclToken
from .tokens.token_type import TokenType
from .utils.ast import AST
from .utils.stream import Stream


class AstGenerator:
    def __init__(self, token_stream: Stream[Token]):
        self._token_stream: Stream[Token] = token_stream
        self._tokens: list[Token] = token_stream.objects

        # some variables to store the state of the ast generator
        self._current_index: int = 0

    def current(self) -> Token:
        """returns the token at the current location"""
        return self._tokens[self._current_index]

    def previous(self) -> Token:
        """returns the previous (consumed) token"""
        if self._current_index == 0:
            raise AstError("can't call previous when no tokens have been consumed yet!")
        return self._tokens[self._current_index - 1]

    def is_at_end(self) -> bool:
        """check whether we are at the end of the token stream, or EOF token"""
        # check for end of token stream
        if self._current_index >= len(self._tokens):
            return True
        return self.current().token_type == TokenType.EOF

    def consume(self) -> Token:
        """consumes the token at the current location"""
        self._current_index += 1
        if self._current_index > len(self._tokens):
            raise AstError("unexpected end-of-file, can't consume more tokens!")
        return self.previous()

    def match(self, *token_types: TokenType) -> Token | None:
        """returns the token if the provided token_type matches the current token"""
        if self.current().token_type in token_types:
            return self.consume()
        return None

    def expect(self, token_type: TokenType, message: str = "") -> None:
        """expects the next token to be of token_type, raises AstError otherwise"""
        if not self.match(token_type):
            if not message:
                message = f"expected {token_type} but found {self.current()}"
            raise AstError(message)

    def expect_newline(self, type_: str = "statement") -> None:
        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            msg = f"expected a newline or End-Of-File after {type_}"
            raise AstError(f"{msg}, found {self.current()}")

    def statement(self) -> Statement:
        """returns a statement of some kind"""
        # check if we have a variable declaration token, and convert this to a statement
        if var_decl_token := self.match(TokenType.VAR_DECL):
            # make sure the type is correct to please the type analyzer
            assert type(var_decl_token) is VarDeclToken

            # check if there is an initial value, fall back to None
            initial_value: Expression | None = None
            if self.match(TokenType.EQUAL):
                initial_value = self.expression()

            # statements should end with a newline
            self.expect_newline()

            return VarDeclStatement(var_decl_token, initial_value)

        # check if we have an identifier token
        if identifier := self.match(TokenType.IDENTIFIER):
            # make sure the type is correct to please the type analyzer
            assert type(identifier) is IdentifierToken

            # check if there is an assignment
            value: Expression | None = None
            if self.match(TokenType.EQUAL):
                value = self.expression()

            # statements should end with a newline
            self.expect_newline()

            # return either an empty statement or an assignment
            if value:
                return AssignmentStatement(identifier, value)
            else:
                return IdentifierStatement(identifier)

        # temporary(!) print statement, printing an expression
        # TODO: replace this temporary statement with a builtin function :)
        if self.match(TokenType.PRINT):
            value = self.expression()

            # statements should end with a newline
            self.expect_newline()

            return PrintStatement(value)

        # TODO:
        # statements starting with a keyword

        # fall back to a bare expression statement
        expression: Expression = self.expression()
        self.expect_newline("expression")

        return ExpressionStatement(expression)

    def expression(self) -> Expression:
        """returns an expression, starts parsing at the lowest precedence level"""
        expression: Expression = self.additive()
        return expression

    def additive(self) -> Expression:
        """returns a PLUS/MINUS, or a higher precedence level expression"""
        # go up the precedence list to get the left hand side expression
        expression: Expression = self.multiplicative()

        while token := self.match(TokenType.PLUS, TokenType.MINUS):
            # we found a plus/minus token, go up the precedence list to get another expression
            right: Expression = self.multiplicative()
            expression = BinaryExpression(expression, token, right)

        # otherwise return the expression found in the beginning
        return expression

    def multiplicative(self) -> Expression:
        """returns a STAR/SLASH, or a higher precedence level expression"""
        # go up the precedence list to get the left hand side expression
        expression: Expression = self.primary()

        while token := self.match(TokenType.STAR, TokenType.SLASH):
            # we found a star/slash token, go up the precedence list to get another expression
            right: Expression = self.primary()
            expression = BinaryExpression(expression, token, right)

        # otherwise return the expression found in the beginning
        return expression

    def primary(self) -> Expression:
        """returns a primary expression: primary keywords or number/string"""
        # match the primary keywords
        if token := self.match(TokenType.FALSE):
            return TokenExpression(token)
        if token := self.match(TokenType.NULL):
            return TokenExpression(token)
        if token := self.match(TokenType.TRUE):
            return TokenExpression(token)

        # match literal numbers and strings
        if token := self.match(TokenType.NUMBER):
            return TokenExpression(token)
        if token := self.match(TokenType.STRING):
            return TokenExpression(token)

        # match expressions between parenthesis
        if token := self.match(TokenType.PAREN_OPEN):
            expression: Expression = self.expression()
            message = f"expected closing parenthesis, but found {self.current()}"
            self.expect(TokenType.PAREN_CLOSE, message)
            return UnaryExpression(ExpressionType.GROUPING, expression)

        # match boolean not expression
        if token := self.match(TokenType.NOT):
            expression: Expression = self.primary()
            return UnaryExpression(ExpressionType.NOT, expression)

        # otherwise we have an error, there must be an expression here
        raise AstError(f"expected an expression, found {self.current()}")

    def generate(self) -> AST:
        """parses the token stream to a list of statements, until EOF is reached"""
        ast: AST = AST()
        while not self.is_at_end():
            ast.append(self.statement())
        return ast
