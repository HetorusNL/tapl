#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from .statement import Statement
from ..tokens.token import Token
from ..utils.source_location import SourceLocation


class ForLoopStatement(Statement):
    """class for a for-loop statement in the form of:

    for(init; check; loop) {statements}
    """

    def __init__(
        self,
        token: Token,
        init: Statement | None,
        check: Expression | None,
        loop: Expression | None,
        statements: list[Statement],
    ):
        # formulate the source location of the for loop
        source_location: SourceLocation = token.source_location
        if init:
            source_location += init.source_location
        if check:
            source_location += check.source_location
        if loop:
            source_location += loop.source_location
        for statement in statements:
            source_location += statement.source_location
        super().__init__(source_location)

        # store the rest of the variables in the class
        self.init: Statement | None = init
        self.check: Expression | None = check
        self.loop: Expression | None = loop
        self.statements: list[Statement] = statements

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
        string: str = f"<ForLoopStatement: location {self.source_location},"
        string += f" {self.init.__repr__()} {self.check.__repr__()} {self.loop.__repr__()}>"
        return string
