from .expression import Expression
from .expression_type import ExpressionType


class UnaryExpression(Expression):
    def __init__(self, expression_type: ExpressionType, expression: Expression):
        self._expression_type: ExpressionType = expression_type
        self._expression: Expression = expression

    @property
    def expression_type(self) -> ExpressionType:
        return self._expression_type

    @expression_type.setter
    def expression_type(self, expression_type: ExpressionType) -> None:
        self._expression_type: ExpressionType = expression_type

    @property
    def expression(self) -> Expression:
        return self._expression

    @expression.setter
    def expression(self, expression: Expression) -> None:
        self._expression: Expression = expression

    def c_code(self) -> str:
        match self.expression_type:
            case ExpressionType.GROUPING:
                return f"({self.expression.c_code()})"
            case ExpressionType.NOT:
                return f"(!({self.expression.c_code()}))"
            # case _ as default:
            #     assert False, f"{self.expjression_type} not in UnaryExpression!"

    def __str__(self) -> str:
        return f"({self.expression})"

    def __repr__(self) -> str:
        return f"<UnaryExpression {self.expression}>"
