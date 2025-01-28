from ..statements import Statement


class AST:
    def __init__(self):
        # the AST consists of a list of statements
        self.statements: list[Statement] = []

    def append(self, statement: Statement) -> None:
        self.statements.append(statement)
