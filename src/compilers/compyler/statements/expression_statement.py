from ..expressions import Expression
from .statement import Statement


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        super().__init__()
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression

    @expression.setter
    def expression(self, expression: Expression) -> None:
        self._expression = expression

    def c_code(self) -> str:
        return self.expression.c_code()

    def __str__(self) -> str:
        return self.expression.__str__()

    def __repr__(self) -> str:
        return f"<ExpressionStatement {self.expression.__repr__()}>"
