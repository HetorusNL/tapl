#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .tapl_error import TaplError
from ..utils.colors import Colors


class AstError(TaplError):
    def __init__(self, message: str, filename: str, line: int, source_line: str):
        # construdt the separate sections of the error message
        newline: str = f"{Colors.RESET}\n"
        file_path: str = f"{Colors.BOLD}{filename}:{line}:{Colors.RESET}"
        error: str = f"{Colors.BOLD}{Colors.RED}error:{Colors.RESET}"

        # construct the error message itself
        error_str: str = f"{newline}{file_path} {error} {message}\n"
        error_str += f"{line:>4d} | {source_line}"

        # pass it to the base class
        super().__init__(error_str)
