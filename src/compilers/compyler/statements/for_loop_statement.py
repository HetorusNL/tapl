#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement


class ForLoopStatement(Statement):
    """class for a for-loop statement in the form of:

    for(init; check; loop) {statements}
    """

    def __init__(
        self, init: Statement | None, check: Expression | None, loop: Expression | None, statements: list[Statement]
    ):
        super().__init__()
        self._init: Statement | None = init
        self._check: Expression | None = check
        self._loop: Expression | None = loop
        self._statements: list[Statement] = statements

    @property
    def init(self) -> Statement | None:
        return self._init

    @init.setter
    def init(self, init: Statement) -> None:
        self._init: Statement | None = init

    @property
    def check(self) -> Expression | None:
        return self._check

    @check.setter
    def check(self, check: Expression) -> None:
        self._check: Expression | None = check

    @property
    def loop(self) -> Expression | None:
        return self._loop

    @loop.setter
    def loop(self, loop: Expression) -> None:
        self._loop: Expression | None = loop

    @property
    def statements(self) -> list[Statement]:
        return self._statements

    @statements.setter
    def statements(self, statements: list[Statement]) -> None:
        self._statements: list[Statement] = statements

    def c_code(self) -> str:
        # construct the for-loop statement
        init_code: str = self.init.c_code() if self.init else ""
        check_code: str = self.check.c_code() if self.check else ""
        loop_code: str = self.loop.c_code() if self.loop else ""

        # strip the ';' if it is already in the init_code
        init_code = init_code.removesuffix(";")

        # add the for-loop statement itself
        code: str = f"for ({init_code}; {check_code}; {loop_code}) {{\n"

        # followed by the statements in the for-loop block
        for statement in self.statements:
            code += f"{statement.c_code()}\n"

        # and end with the closing brace
        code += f"}}"
        return code

    def __str__(self) -> str:
        return f"for ({self.init.__str__()}; {self.check.__str__()}; {self.loop.__str__()}): ..."

    def __repr__(self) -> str:
        return f"<ForLoopStatement {self.init.__repr__()} {self.check.__repr__()} {self.loop.__repr__()}>"
