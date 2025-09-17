#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from .colors import Colors
from .source_location import SourceLocation


class Utils:
    """Utility class with several class methods"""

    @classmethod
    def get_source_line_number(cls, filename: Path, source_location: SourceLocation | None) -> int:
        # initial check if a valid SourceLocation is passed
        if not source_location:
            return -1

        # read the entire file info a string
        with open(filename) as f:
            content: str = f.read()

        # sanity check that the SourceLocation start is within the file
        if source_location.start > len(content):
            return -1

        # return the number of newlines until the SourceLocation start
        location_start: int = source_location.start + 1
        return content[:location_start].count("\n")

    @classmethod
    def get_source_line(cls, filename: Path, line: int):
        no_source: str = f"<no source code line available>"
        # initial check if a valid line is passed
        if line < 0:
            return no_source

        # read the file into lines
        with open(filename) as f:
            lines: list[str] = f.readlines()

        # check if the line number exists in the file, return the correct line or error
        if line <= len(lines):
            return lines[line - 1].removesuffix("\n")
        else:
            error = f"[ internal compiler error! (line {line} not found in source) ]"
            return f"{Colors.BOLD}{Colors.RED}{error}{Colors.RESET} {no_source}"
