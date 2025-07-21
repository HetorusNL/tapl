#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from .colors import Colors


class Utils:
    """Utility class with several class methods"""

    @classmethod
    def get_source_line(cls, filename: Path, line: int):
        no_source: str = f"<no source code line available>"
        if line >= 0:
            with open(filename) as f:
                lines: list[str] = f.readlines()
                if line > 0 and line <= len(lines):
                    return lines[line - 1].removesuffix("\n")
                else:
                    error = f"[ internal compiler error! (line {line} not found in source) ]"
                    return f"{Colors.BOLD}{Colors.RED}{error}{Colors.RESET} {no_source}"
        else:
            return no_source
