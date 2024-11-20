from ..token_type import TokenType
from .token import Token


class NumberToken(Token):
    def __init__(self, line: int, value: int):
        super().__init__(TokenType.NUMBER, line)
        # store the additional properties in the class
        self._value: int = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"<{self.token_type}: line {self.line}, {self.value}>"
