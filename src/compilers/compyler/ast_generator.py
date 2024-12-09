from .errors import AstError
from .expressions import Expression
from .tokens import Token
from .tokens.token_type import TokenType


class AstGenerator:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens

        # some variables to store the state of the ast generator
        self._current_index: int = 0
        self._expressions: list[Expression] = []

    def consume(self) -> Token:
        self._current_index += 1
        if self._current_index >= len(self._expressions):
            raise AstError("unexpected end-of-file, can't consume more tokens!")
        return self._tokens[self._current_index]

    def previous(self) -> Token:
        if self._current_index == 0:
            raise AstError("can't call previous when no tokens have been consumed yet!")
        return self._tokens[self._current_index - 1]

    def match(self, token_type: TokenType) -> Token | None:
        if self._tokens[self._current_index].token_type == token_type:
            return self.consume()
        return None

    def expression(self):
        expression: Expression = self.primary()
        return expression

    def primary(self) -> Expression:
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
        raise AstError("expected an expression!")

    def generate(self) -> list[Expression]:
        self._expressions.append(self.expression())
        return self._expressions
