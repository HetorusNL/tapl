#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..utils.ast import AST
from .scoping_pass import ScopingPass
from .typing_pass import TypingPass


class AstCheck:
    def __init__(self, ast: AST):
        self._ast: AST = ast

    def run(self) -> None:
        """run several passes on the AST to perform a variety of checks on the statements"""
        # check the variables defined in the scopes of the AST
        ScopingPass(self._ast).run()
        # check and apply types to the variables, including type 'upscaling'
        TypingPass(self._ast).run()
        # check that all expressions have a type
        TypingPass(self._ast).verify_types()
