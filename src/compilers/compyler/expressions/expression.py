from ..tokens import NumberToken
from ..tokens import StringToken
from ..tokens import Token
from ..tokens.token_type import TokenType


class Expression:
    def __init__(self, token: Token):
        self._token: Token = token

    @property
    def token(self) -> Token:
        return self._token

    @token.setter
    def token(self, token: Token) -> None:
        self._token: Token = token

    def c_code(self) -> str:
        match self._token.token_type:
            # handle the special cases
            case TokenType.NUMBER:
                assert isinstance(self._token, NumberToken)
                return str(self._token.value)
            case TokenType.STRING:
                assert isinstance(self._token, StringToken)
                return self._token.value
            # fall back to the string representation of the token type
            case _:
                return self._token.token_type.value

    def __str__(self) -> str:
        return f"{self._token}"

    def __repr__(self) -> str:
        return f"<Expression {self._token}>"
