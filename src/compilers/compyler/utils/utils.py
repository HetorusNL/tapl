#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from .colors import Colors
from .source_location import SourceLocation
from ..types.character_type import CharacterType
from ..types.numeric_type import NumericType
from ..types.numeric_type_type import NumericTypeType
from ..types.type import Type


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
        location_start: int = source_location.start
        return content[:location_start].count("\n") + 1

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

    @classmethod
    def get_type_format_string(cls, type_: Type):
        match type_:
            case CharacterType():
                return f"%c"
            case NumericType():
                # depending on the size of the type, add 'l' to the format
                long: str = "l" if type_.num_bits > 32 else ""
                match type_.numeric_type_type:
                    case NumericTypeType.SIGNED:
                        return f"%{long}d"
                    case NumericTypeType.UNSIGNED:
                        return f"%{long}u"
                    case NumericTypeType.FLOATING_POINT:
                        return f"%{long}f"
            case _:
                assert False, f"internal compiler error, {type(type_)} not handled!"
