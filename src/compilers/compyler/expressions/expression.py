from ..tokens import Token


class Expression:
    def __init__(self, token: Token):
        self._token: Token = token

    @property
    def token(self) -> Token:
        return self._token

    @token.setter
    def token(self, token: Token) -> None:
        self._token: Token = token

    def __str__(self) -> str:
        return f"({self._token})"

    def __repr__(self) -> str:
        return f"<Expression {self._token}>"
