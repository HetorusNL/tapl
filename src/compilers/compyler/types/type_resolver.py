from ..tokens import Token
from .types import Types


class TypeResolver:
    def __init__(self, tokens: list[Token]):
        self._tokens: list[Token] = tokens

    def resolve(self) -> Types:
        types: Types = Types()
        # TODO: loop through the tokens and extract the types
        return types
