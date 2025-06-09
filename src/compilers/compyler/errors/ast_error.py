#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..utils.colors import Colors


class AstError(BaseException):
    def __init__(self, message: str, line: int, source_line: str):
        remove_me: str = f"{Colors.RESET}\n"  # TODO: remove after taking care of errors during compilation
        filename: str = f"{remove_me}{Colors.BOLD}/path/to/file:{line}:{Colors.RESET}"
        error: str = f"{Colors.BOLD}{Colors.RED}error:{Colors.RESET}"
        error_str: str = f"{filename} {error} {message}\n"
        error_str += f"{line:>4d} | {source_line}"
        super().__init__(error_str)
