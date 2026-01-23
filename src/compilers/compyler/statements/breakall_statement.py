#!/usr/bin/env python
#
# Copyright (c) 2026 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .statement import Statement
from ..utils.source_location import SourceLocation


class BreakallStatement(Statement):
    def __init__(self, source_location: SourceLocation, breakall_label: str):
        super().__init__(source_location)

        # store the rest of the variables in the class
        self.breakall_label: str = breakall_label

    def c_code(self) -> str:
        return "goto " + self.breakall_label + ";"

    def __str__(self) -> str:
        return "breakall"

    def __repr__(self) -> str:
        return f"<BreakallStatement: location {self.source_location}, {self.breakall_label}>"
