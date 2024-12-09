from .errors import AstError
from .expressions import BinaryExpression
from .expressions import Expression
from .tokens import Token
from .tokens.token_type import TokenType


class AstGenerator:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens

        # some variables to store the state of the ast generator
        self._current_index: int = 0
        self._expressions: list[Expression] = []

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

        if token := self.match(TokenType.STAR, TokenType.SLASH):
            # we found a star token, go up the precedence list to get another expression
            right: Expression = self.primary()
            expression = BinaryExpression(expression, token, right)

        # otherwise return the expression found in the beginning
        return expression

    def primary(self) -> Expression:
        """returns a primary expression: primary keywords or number/string"""
        # match the primary keywords
        if token := self.match(TokenType.FALSE):
            return Expression(token)
        if token := self.match(TokenType.NULL):
            return Expression(token)
        if token := self.match(TokenType.TRUE):
            return Expression(token)

        # match literal numbers and strings
        if token := self.match(TokenType.NUMBER):
            return Expression(token)
        if token := self.match(TokenType.STRING):
            return Expression(token)

        # otherwise we have an error, there must be an expression here
        raise AstError(f"expected an expression, found {self.current()}")

    def generate(self) -> list[Expression]:
        """parses the token stream to a list of expressions, until EOF is reached"""
        while not self.is_at_end():
            self._expressions.append(self.expression())
        return self._expressions
