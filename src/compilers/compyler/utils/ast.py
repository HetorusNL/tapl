from ..statements import Statement
from .stream import Stream


class AST:
    def __init__(self):
        # the AST consists of a statements stream
        self.statements: Stream[Statement] = Stream()

    def append(self, *statements: Statement) -> None:
        self.statements.add(*statements)
