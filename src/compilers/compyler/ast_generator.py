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
from .statements.for_loop_statement import ForLoopStatement
from .statements.if_statement import IfStatement
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

    def next(self) -> Token:
        """returns the token after the current location"""
        if self._current_index + 1 > len(self._tokens):
            raise AstError("unexpected end-of-file, next token doesn't exist!")
        return self._tokens[self._current_index + 1]

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

    def expect(self, token_type: TokenType, message: str = "") -> Token:
        """expects the next token to be of token_type, return token if match, raises AstError otherwise"""
        if token := self.match(token_type):
            return token
        else:
            if not message:
                message = f"expected {token_type} but found {self.current()} at line {self.current().line}"
            raise AstError(message)

    def expect_newline(self, type_: str = "statement", must_end_with_newline: bool = True) -> None:
        if not must_end_with_newline:
            return

        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            msg = f"expected a newline or End-Of-File after {type_}"
            raise AstError(f"{msg}, found {self.current()} at line {self.current().line}")

    def _has_indent(self) -> bool:
        """returns whether the next token is an indent, if so, consume it"""
        # if we're at EOF, there is no indent
        if self.is_at_end():
            return False

        # if the next token is an indent, consume it
        return self.match(TokenType.INDENT) is not None

    def _statement_block(self) -> list[Statement]:
        """returns a list of statements in the block, list is empty if there is no indent"""
        # we can either have an empty block or we must have an indent
        if not self._has_indent():
            return []

        # capture all statements until we get a dedent
        statements: list[Statement] = []
        while not self.match(TokenType.DEDENT):
            statement: Statement = self.statement()
            statements.append(statement)
        return statements

    def assignment_statement(self, must_end_with_newline: bool) -> AssignmentStatement | None:
        # check (but don't consume) if we have an identifier token
        if self.current().token_type != TokenType.IDENTIFIER:
            return
        # check if there is an assignment (still no consuming)
        if self.next().token_type != TokenType.EQUAL:
            return

        # this is an assignment, consume the identifier
        identifier = self.match(TokenType.IDENTIFIER)
        # make sure the type is correct to please the type analyzer
        assert type(identifier) is IdentifierToken

        # consume the equal
        self.expect(TokenType.EQUAL)

        # then consume the expression
        value: Expression = self.expression()

        # statements should end with a newline
        self.expect_newline(must_end_with_newline=must_end_with_newline)

        # return the assignment statement
        return AssignmentStatement(identifier, value)

    def for_statement(self) -> ForLoopStatement | None:
        # early return if we don't have a for-loop statement
        if not self.match(TokenType.FOR):
            return None

        # otherwise we have an (already consumed) for-loop statement
        # start parsing the initial value statement (if it exists)
        init: Statement | None = None
        if not self.match(TokenType.SEMICOLON):
            init: Statement | None = self.statement(must_end_with_newline=False)
            self.match(TokenType.SEMICOLON)

        # parse the check expression (if it exists)
        check: Expression | None = None
        if not self.match(TokenType.SEMICOLON):
            check: Expression | None = self.expression()
            self.match(TokenType.SEMICOLON)

        # parse the loop expression (if it exists)
        loop: Expression | None = None
        if not self.match(TokenType.COLON):
            loop: Expression | None = self.expression()
            self.match(TokenType.COLON)

        # followed by a newline
        self.expect_newline()

        # continue with the body of the for-loop statement
        statements: list[Statement] = self._statement_block()

        # return the finished for-loop statement
        return ForLoopStatement(init, check, loop, statements)

    def single_if_statement(self, if_statement: IfStatement | None = None) -> IfStatement | None:
        # early return if we don't have an if statement
        if not self.match(TokenType.IF):
            return None

        # otherwise we have an (already consumed) if statement
        # start parsing the if statement line itself
        # first match an expression
        expression: Expression = self.expression()
        # then a colon
        self.expect(TokenType.COLON)
        # followed by a newline
        self.expect_newline()

        # continue with the body of the statement
        statements: list[Statement] = self._statement_block()

        # if we already got an if statement, add it as else-if block
        if if_statement:
            if_statement.add_else_if_statement_block(expression, statements)
            return if_statement

        # otherwise return a new if statement
        return IfStatement(expression, statements)

    def if_statement(self) -> IfStatement | None:
        statement: IfStatement | None = self.single_if_statement()
        # return the if statement if we found an EOF, or None if we didn't find a if statement
        if self.is_at_end() or not statement:
            return statement

        # check for else-if and else blocks
        while self.match(TokenType.ELSE):
            # check for another if, an else-if block
            if self.single_if_statement(statement):
                # found an else-if block, it has already been added, so loop back to search for more
                pass
            else:
                # found a bare else, this is the final statement block
                # first expect a colon
                self.expect(TokenType.COLON)
                # followed by a newline
                self.expect_newline()

                # now parse the statements
                statements: list[Statement] = self._statement_block()

                # add this block as the else statements to the if statement
                statement.else_statements = statements
                # nothing more in an if statement after an else, so break from the loop
                break

        # no (more) else statements, return the finished if statement
        return statement

    def print_statement(self) -> PrintStatement | None:
        # early return if we don't have a print statement
        if not self.match(TokenType.PRINT):
            return

        # match an expression between parenthesis
        self.match(TokenType.PAREN_OPEN)
        value = self.expression()
        self.match(TokenType.PAREN_CLOSE)

        # statements should end with a newline
        self.expect_newline()

        return PrintStatement(value)

    def var_decl_statement(self, must_end_with_newline: bool) -> VarDeclStatement | None:
        # check if we have a variable declaration token, and convert this to a statement
        if var_decl_token := self.match(TokenType.VAR_DECL):
            # make sure the type is correct to please the type analyzer
            assert type(var_decl_token) is VarDeclToken

            # check if there is an initial value, fall back to None
            initial_value: Expression | None = None
            if self.match(TokenType.EQUAL):
                initial_value = self.expression()

            # statements should end with a newline
            self.expect_newline(must_end_with_newline=must_end_with_newline)

            return VarDeclStatement(var_decl_token, initial_value)

    def statement(self, must_end_with_newline: bool = True) -> Statement:
        """returns a statement of some kind"""
        # check for a variable declaration statement
        if statement := self.var_decl_statement(must_end_with_newline):
            return statement

        # check for an assignment statement
        if statement := self.assignment_statement(must_end_with_newline):
            return statement

        # temporary(!) print statement, printing an expression
        # TODO: replace this temporary statement with a builtin function :)
        if statement := self.print_statement():
            return statement

        # check for an if statement
        if statement := self.if_statement():
            return statement

        # check for a for-loop statement
        if statement := self.for_statement():
            return statement

        # TODO:
        # more statements starting with a keyword

        # fall back to a bare expression statement
        expression: Expression = self.expression()
        self.expect_newline("expression")

        return ExpressionStatement(expression)

    def expression(self) -> Expression:
        """returns an expression, starts parsing at the lowest precedence level"""
        expression: Expression = self.boolean()
        return expression

    def boolean(self) -> Expression:
        """returns a boolean expression, or a higher precedence level expression"""
        # go up the precedence list to get the left hand side expression
        expression: Expression = self.additive()

        boolean_expression_tokens: tuple[TokenType, ...] = (
            TokenType.EQUAL_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.NOT_EQUAL,
        )
        while token := self.match(*boolean_expression_tokens):
            # we found a boolean expression token, go up the precedence list go get another expression
            right: Expression = self.additive()
            expression = BinaryExpression(expression, token, right)

        # otherwise return the expression found at the beginning
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
            message = f"expected closing parenthesis, but found {self.current()} at line {self.current().line}"
            self.expect(TokenType.PAREN_CLOSE, message)
            return UnaryExpression(ExpressionType.GROUPING, expression)

        # match boolean not expression
        if token := self.match(TokenType.NOT):
            expression: Expression = self.primary()
            return UnaryExpression(ExpressionType.NOT, expression)

        # match unary minus expression
        if token := self.match(TokenType.MINUS):
            expression: Expression = self.primary()
            return UnaryExpression(ExpressionType.MINUS, expression)

        # match pre increment or decrement expression
        if token := self.match(TokenType.INCREMENT):
            identifier: Token = self.expect(TokenType.IDENTIFIER)
            expression: Expression = TokenExpression(identifier)
            return UnaryExpression(ExpressionType.PRE_INCREMENT, expression)
        if token := self.match(TokenType.DECREMENT):
            identifier: Token = self.expect(TokenType.IDENTIFIER)
            expression: Expression = TokenExpression(identifier)
            return UnaryExpression(ExpressionType.PRE_DECREMENT, expression)

        # match an identifier
        if token := self.match(TokenType.IDENTIFIER):
            expression: Expression = TokenExpression(token)
            # check for increment and decrement
            if self.match(TokenType.INCREMENT):
                return UnaryExpression(ExpressionType.POST_INCREMENT, expression)
            if self.match(TokenType.DECREMENT):
                return UnaryExpression(ExpressionType.POST_DECREMENT, expression)
            # otherwise return the bare token expression
            return expression

        # otherwise we have an error, there must be an expression here
        raise AstError(f"expected an expression, found {self.current()} at line {self.current().line}")

    def generate(self) -> AST:
        """parses the token stream to a list of statements, until EOF is reached"""
        ast: AST = AST()
        while not self.is_at_end():
            ast.append(self.statement())
        return ast
