from .token_type import TokenType


class Token:
    def __init__(self, token_type: TokenType, line: int):
        self._token_type: TokenType = token_type
        self._line: int = line

    @property
    def token_type(self) -> TokenType:
        return self._token_type

    @token_type.setter
    def token_type(self, token_type: TokenType) -> None:
        self._token_type: TokenType = token_type

    @property
    def line(self) -> int:
        return self._line

    @line.setter
    def line(self, line: int) -> None:
        self._line: int = line

    def __str__(self) -> str:
        return f"{self.token_type}"

    def __repr__(self) -> str:
        return f"<{self.token_type}: line {self.line}>"
