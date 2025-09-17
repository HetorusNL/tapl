#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from ..statements.statement import Statement
from .stream import Stream
from ..types.types import Types


class AST:
    def __init__(self, filename: Path, types: Types):
        # the AST consists of a statements stream
        self.statements: Stream[Statement] = Stream()
        # also store the filename where the AST is generated from
        self.filename: Path = filename
        # store the rest of the data in the class
        self.types: Types = types

    def append(self, *statements: Statement) -> None:
        self.statements.add(*statements)
