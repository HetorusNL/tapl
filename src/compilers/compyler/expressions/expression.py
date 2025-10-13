#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..utils.source_location import SourceLocation


class Expression:
    def __init__(self, source_location: SourceLocation):
        self.source_location: SourceLocation = source_location

    def c_code(self) -> str:
        assert False, f"we can't generate code for a {type(self)}!"

    def __str__(self) -> str:
        return f""

    def __repr__(self) -> str:
        return f"<Expression: location {self.source_location}>"
