#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path
from typing import NoReturn

from .errors.tapl_error import TaplError
from .errors.ast_error import AstError
from .expressions.binary_expression import BinaryExpression
from .expressions.call_expression import CallExpression
from .expressions.expression import Expression
from .expressions.unary_expression import UnaryExpression
from .expressions.token_expression import TokenExpression
from .expressions.type_cast_expression import TypeCastExpression
from .expressions.expression_type import ExpressionType
from .statements.assignment_statement import AssignmentStatement
from .statements.expression_statement import ExpressionStatement
from .statements.for_loop_statement import ForLoopStatement
from .statements.function_statement import FunctionStatement
from .statements.if_statement import IfStatement
from .statements.print_statement import PrintStatement
from .statements.return_statement import ReturnStatement
from .statements.statement import Statement
from .statements.var_decl_statement import VarDeclStatement
from .tokens.identifier_token import IdentifierToken
from .tokens.token import Token
from .tokens.type_token import TypeToken
from .tokens.token_type import TokenType
from .types.types import Types
from .utils.ast import AST
from .utils.colors import Colors
from .utils.stream import Stream
from .utils.utils import Utils


class AstGenerator:
    def __init__(self, filename: Path, token_stream: Stream[Token], types: Types):
        self._token_stream: Stream[Token] = token_stream
        self._tokens: list[Token] = token_stream.objects
        self._filename: Path = filename
        self._types: Types = types

        # some variables to store the state of the ast generator
        self._current_index: int = 0
        self._can_return: bool = False

    def current(self) -> Token:
        """returns the token at the current location"""
        return self._tokens[self._current_index]

    def next(self, offset: int = 1) -> Token:
        """returns the token after the current location, or at the offset, if offset is provided"""
        if self._current_index + offset > len(self._tokens):
            self.ast_error(f"unexpected end-of-file, token at offset {offset} doesn't exist!")
        return self._tokens[self._current_index + offset]

    def previous(self) -> Token:
        """returns the previous (consumed) token"""
        if self._current_index == 0:
            self.ast_error("can't call previous when no tokens have been consumed yet!")
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
            self.ast_error("unexpected end-of-file, can't consume more tokens!")
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
                message = f"expected '{token_type}' but found '{self.current()}'!"
            self.ast_error(message)

    def expect_newline(self, type_: str = "statement", must_end_with_newline: bool = True) -> None:
        if not must_end_with_newline:
            return

        if not self.match(TokenType.NEWLINE, TokenType.EOF):
            self.ast_error(f"expected a newline or End-Of-File after {type_}, found '{self.current()}'!")

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

    def for_loop_statement(self) -> ForLoopStatement | None:
        # early return if we don't have a for-loop statement
        if not self.match(TokenType.FOR):
            return None

        # otherwise we have an (already consumed) for-loop statement
        # start parsing the initial value statement (if it exists)
        init: Statement | None = None
        if not self.match(TokenType.SEMICOLON):
            init: Statement | None = self.statement(must_end_with_newline=False)
            self.expect(TokenType.SEMICOLON)

        # parse the check expression (if it exists)
        check: Expression | None = None
        if not self.match(TokenType.SEMICOLON):
            check: Expression | None = self.expression()
            self.expect(TokenType.SEMICOLON)

        # parse the loop expression (if it exists)
        loop: Expression | None = None
        if not self.match(TokenType.COLON):
            loop: Expression | None = self.expression()
            self.expect(TokenType.COLON)

        # followed by a newline
        self.expect_newline()

        # continue with the body of the for-loop statement
        statements: list[Statement] = self._statement_block()

        # return the finished for-loop statement
        return ForLoopStatement(init, check, loop, statements)

    def _type_statement(self, must_end_with_newline: bool) -> FunctionStatement | VarDeclStatement | None:
        """returns a statement starting with a type, or None otherwise"""
        # start with a type
        if self.current().token_type != TokenType.TYPE:
            return None
        # the next common token is an identifier
        if self.next(1).token_type != TokenType.IDENTIFIER:
            return None

        # check if we have a function that has an opening paren here
        # no need to handle parsing past-EOF here, as this is token exists in the stream
        if self.next(2).token_type == TokenType.PAREN_OPEN:
            return self.function_statement()

        # otherwise we have an variable declaration statement
        return self.var_decl_statement(must_end_with_newline)

    def _finish_function_statement(self, function_statement: FunctionStatement) -> FunctionStatement:
        # after the function definition itself, we expect a colon
        self.expect(TokenType.COLON)
        # followed by a newline
        self.expect_newline()

        # we're inside a function, allow return statements here
        self._can_return = True

        # continue with the body of the function
        statements: list[Statement] = self._statement_block()
        # add them to the function
        function_statement.statements = statements

        # we've finished parsing the function statements, don't allow return statements from now on
        self._can_return = False

        # return the finished function statement
        return function_statement

    def function_statement(self) -> FunctionStatement:
        # the _type_statement function already checked the tokens for us
        # so we can start consuming here
        return_type: Token = self.consume()
        assert type(return_type) == TypeToken
        name: Token = self.consume()
        assert type(name) == IdentifierToken
        function_statement: FunctionStatement = FunctionStatement(return_type, name)
        self.expect(TokenType.PAREN_OPEN)

        # check for a closing parenthesis, then we have a function without arguments
        if self.match(TokenType.PAREN_CLOSE):
            # finish parsing and return the function statement
            return self._finish_function_statement(function_statement)

        # consume type-name function arguments
        while True:
            argument_type: Token = self.expect(TokenType.TYPE)
            assert type(argument_type) == TypeToken
            # test that the argument type is non-void
            if not argument_type.type_.non_void():
                self.ast_error("function arguments cannot be of type void!")
            argument_name: Token = self.expect(TokenType.IDENTIFIER)
            assert type(argument_name) == IdentifierToken
            # add the argument to the function statement
            function_statement.add_argument(argument_type, argument_name)

            # if we don't have a comma, it's the end of the argument list
            if not self.match(TokenType.COMMA):
                break

        # we must end with a closing parenthesis
        self.expect(TokenType.PAREN_CLOSE)

        # finish parsing and return the function statement
        return self._finish_function_statement(function_statement)

    def _single_if_statement(self, if_statement: IfStatement | None = None) -> IfStatement | None:
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
        statement: IfStatement | None = self._single_if_statement()
        # return the if statement if we found an EOF, or None if we didn't find a if statement
        if self.is_at_end() or not statement:
            return statement

        # check for else-if and else blocks
        while self.match(TokenType.ELSE):
            # check for another if, an else-if block
            if self._single_if_statement(statement):
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
        self.expect(TokenType.PAREN_OPEN)
        value = self.expression()
        self.expect(TokenType.PAREN_CLOSE)

        # statements should end with a newline
        self.expect_newline()

        return PrintStatement(value)

    def return_statement(self) -> ReturnStatement | None:
        # early return if we don't have a return statement
        if not self.match(TokenType.RETURN):
            return

        # check if we're allowed to return, error otherwise
        if not self._can_return:
            self.ast_error(f"return statement is not allowed here!")

        # check if we have a newline
        if self.match(TokenType.NEWLINE, TokenType.EOF):
            # return the statement without value
            return ReturnStatement()

        # otherwise expect an expression to return
        expression: Expression = self.expression()

        # statements should end with a newline
        self.expect_newline()

        return ReturnStatement(expression)

    def var_decl_statement(self, must_end_with_newline: bool) -> VarDeclStatement | None:
        # the _type_statement function already checked the tokens for us
        # so we can start consuming here
        type_token: Token = self.consume()
        assert isinstance(type_token, TypeToken)
        name: Token = self.consume()
        assert isinstance(name, IdentifierToken)

        # check if there is an initial value, fall back to None
        initial_value: Expression | None = None
        if self.match(TokenType.EQUAL):
            initial_value: Expression | None = self.expression()

        # statements should end with a newline
        self.expect_newline(must_end_with_newline=must_end_with_newline)

        return VarDeclStatement(type_token, name, initial_value)

    def while_loop_statement(self) -> ForLoopStatement | None:
        # will generate a for loop statement if a while loop is found
        # early return if we don't have a while-loop statement
        if not self.match(TokenType.WHILE):
            return None

        # otherwise we have an (already consumed) while-loop statement
        # parse the condition (to be placed in the check expression of the for-loop statement)
        check: Expression = self.expression()

        # followed by a colon and newline
        self.expect(TokenType.COLON)
        self.expect_newline()

        # continue with the body of the while-loop statement
        statements: list[Statement] = self._statement_block()

        # return the finished while-loop as a for-loop statement
        return ForLoopStatement(None, check, None, statements)

    def statement(self, must_end_with_newline: bool = True) -> Statement:
        """returns a statement of some kind"""
        # check for a statement starting with a type
        if statement := self._type_statement(must_end_with_newline):
            return statement

        # check for a return statement
        if statement := self.return_statement():
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
        if statement := self.for_loop_statement():
            return statement

        # check for a while-loop statement
        if statement := self.while_loop_statement():
            return statement

        # TODO: add classes

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
            # check if this is a type casting
            if type_ := self.match(TokenType.TYPE):
                assert isinstance(type_, TypeToken)
                # expect a closing parenthesis
                self.expect(TokenType.PAREN_CLOSE)
                # followed by a primary expression that is type casted
                primary: Expression = self.primary()
                return TypeCastExpression(type_, primary)

            # otherwise it's a grouping expression
            expression: Expression = self.expression()
            message = f"expected closing parenthesis, but found '{self.current()}'!"
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
            # check for a function call
            if self.match(TokenType.PAREN_OPEN):
                assert isinstance(token, IdentifierToken)
                return self.call_expression(token)
            # otherwise return the bare token expression
            return expression

        # otherwise we have an error, there must be an expression here
        self.ast_error(f"expected an expression, found '{self.current()}'!")

    def call_expression(self, name: IdentifierToken) -> CallExpression:
        # the name is already provided, and the opening parenthesis is consumed

        # check for a closing parenthesis, then we have a function call without arguments
        if self.match(TokenType.PAREN_CLOSE):
            # simply return a call expression without arguments
            return CallExpression(name)

        # otherwise start parsing the arguments
        arguments: list[Expression] = []
        while True:
            # start with the expression
            expression: Expression = self.expression()
            arguments.append(expression)

            # if we don't have a comma, it's the end of the argument list
            if not self.match(TokenType.COMMA):
                break

        # we must end with a closing parenthesis
        self.expect(TokenType.PAREN_CLOSE)

        # construct and return the call expression
        return CallExpression(name, arguments)

    def ast_error(self, message: str) -> NoReturn:
        """constructs and raises an AstError"""
        # fill in the filename that we're compiling
        filename: str = str(self._filename.resolve())

        # extract the line number from the current or previous token
        line: int = -1
        try:
            # try to get the line number from the current token
            line: int = self.current().line
        except IndexError:
            # if that fails (out of bounds), try the previous token
            if self._current_index != 0:  # sanity check for previous()
                line: int = self.previous().line

        # extract the source code line from the file
        source_line: str = Utils.get_source_line(self._filename, line)

        # check for internal compiler error (line == -1)
        if line == -1:
            error: str = f"{Colors.BOLD}{Colors.RED}[ internal compiler error! (line == -1) ]{Colors.RESET}"
            source_line = f"{error} {source_line}"

        raise AstError(message, filename, line, source_line)

    def generate(self) -> AST:
        """parses the token stream to a list of statements, until EOF is reached"""
        errors: list[TaplError] = []
        ast: AST = AST(self._filename, self._types)
        while not self.is_at_end():
            try:
                ast.append(self.statement())
            except TaplError as e:
                errors.append(e)
                # continue until we get to a newline, indicating a new statement
                while not self.match(TokenType.NEWLINE, TokenType.EOF):
                    self.consume()
                # also consume the indent and dedent tokens if they are there
                while self.match(TokenType.INDENT, TokenType.DEDENT):
                    pass

        # if we found errors, print them and exit with exit code 1
        if errors:
            [print(e) for e in errors]
            exit(1)

        return ast
