from .expression import Expression
from ..tokens import Token


class BinaryExpression(Expression):
    def __init__(self, left: Expression, token: Token, right: Expression):
        super().__init__(token)
        self._left: Expression = left
        self._right: Expression = right

    @property
    def left(self) -> Expression:
        return self._left

    @left.setter
    def left(self, left: Expression) -> None:
        self._left: Expression = left

    @property
    def right(self) -> Expression:
        return self._right

    @right.setter
    def right(self, right: Expression) -> None:
        self._right: Expression = right

    def __str__(self) -> str:
        return f"({self.left} {self.token.token_type.value} {self.right})"

    def __repr__(self) -> str:
        return f"<BinaryExpression {self.left} {self.token.token_type} {self.right}>"
