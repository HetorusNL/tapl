#!/usr/bin/env python
#
# Copyright (c) 2026 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .statement import Statement
from ..utils.source_location import SourceLocation


class ContinueStatement(Statement):
    def __init__(self, source_location: SourceLocation):
        super().__init__(source_location)

    def c_code(self) -> str:
        return "continue;"

    def __str__(self) -> str:
        return "continue"

    def __repr__(self) -> str:
        return f"<ContinueStatement: location {self.source_location}>"
