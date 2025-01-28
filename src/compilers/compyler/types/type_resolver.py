from ..tokens import IdentifierToken
from ..tokens import Token
from ..tokens.token_type import TokenType
from .types import Types


class TypeResolver:
    def __init__(self, tokens: list[Token]):
        self._tokens: list[Token] = tokens
        self._tokens_length: int = len(self._tokens)

    def resolve(self) -> Types:
        """resolve all types in the provided token stream.
        returns the builtin types and the resolved types from the tokens stream"""
        types: Types = Types()

        # loop through the tokens to find class declarations and extract the types
        for index, token in enumerate(self._tokens):
            if token.token_type == TokenType.CLASS:
                if index + 1 < self._tokens_length:
                    class_name: Token = self._tokens[index + 1]
                    if isinstance(class_name, IdentifierToken):
                        types.add(class_name.value)

        return types
