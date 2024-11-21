from .token_type import TokenType
from .token import Token


class StringToken(Token):
    def __init__(self, line: int, value: str):
        super().__init__(TokenType.STRING, line)
        # store the additional properties in the class
        self._value: str = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __str__(self) -> str:
        return f'<{self.token_type}: line {self.line}, "{self.value}">'
