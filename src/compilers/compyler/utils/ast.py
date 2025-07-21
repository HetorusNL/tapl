#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from ..statements.statement import Statement
from .stream import Stream


class AST:
    def __init__(self, filename: Path):
        # the AST consists of a statements stream
        self.statements: Stream[Statement] = Stream()
        # also store the filename where the AST is generated from
        self.filename: Path = filename

    def append(self, *statements: Statement) -> None:
        self.statements.add(*statements)
