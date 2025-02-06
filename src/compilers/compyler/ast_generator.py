#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .errors import AstError
from .expressions import BinaryExpression
from .expressions import Expression
from .expressions import UnaryExpression
from .expressions import TokenExpression
from .expressions.expression_type import ExpressionType
from .statements import ExpressionStatement
from .statements import Statement
from .tokens import Token
from .tokens.token_type import TokenType
from .utils import AST
from .utils import Stream


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

    def statement(self) -> Statement:
        """returns a statement"""
        # for now, return a statement as an expression with a trailing newline
        expression: Expression = self.expression()
        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            msg = "expected a newline or End-Of-File after expression"
            raise AstError(f"{msg}, found {self.current()}")
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
