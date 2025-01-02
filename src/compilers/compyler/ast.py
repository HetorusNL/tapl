from .expressions import Expression


class AST:
    def __init__(self):
        # for now the AST consists of a list of expressions
        # TODO: later this will become a list of statements
        self.expressions: list[Expression] = []

    def append(self, expression: Expression) -> None:
        self.expressions.append(expression)
