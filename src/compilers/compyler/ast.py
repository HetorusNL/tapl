from .tokens.token import Token


class AST:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens

    def generate(self) -> None:
        pass
