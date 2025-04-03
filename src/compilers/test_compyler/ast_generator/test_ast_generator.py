#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path
import unittest

from compyler.ast_generator import AstGenerator
from compyler.statements.statement import Statement
from compyler.tokenizer import Tokenizer
from compyler.tokens.token import Token
from compyler.utils.ast import AST
from compyler.utils.stream import Stream


class TestAstGenerator(unittest.TestCase):
    def setUp(self):
        print()

    def test_ast_generator_example_statements(self):
        # make sure to pass a resolved path to the tokenizer and ast generator
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "example_statements.tim"
        tokens: Stream[Token] = Tokenizer(example_file).tokenize()
        ast: AST = AstGenerator(tokens).generate()
        ast_statements: list[Statement] = ast.statements.objects
        print(*ast_statements, sep="\n")

        # or simpler converting the individual statements to str
        result = [
            "(((1100 + (150 * 2)) + 37) - 100);",
            "((1 * 2) + (3 / ((4 + true))));",
            'printf("%d\\n", (1337));',
        ]
        self.assertEqual([statement.c_code() for statement in ast_statements], result)
