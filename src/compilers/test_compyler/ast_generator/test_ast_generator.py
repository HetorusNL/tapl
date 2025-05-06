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
from compyler.types.type_applier import TypeApplier
from compyler.types.type_resolver import TypeResolver
from compyler.types.types import Types
from compyler.utils.ast import AST
from compyler.utils.stream import Stream


class TestAstGenerator(unittest.TestCase):
    def setUp(self):
        print()

    def test_ast_generator_example_statements(self):
        self._run_compilation_test("example_statements.tim", "result_example_statements.txt")

    def test_ast_generator_indentation_tests(self):
        self._run_compilation_test("indentation_tests.tim", "result_indentation_tests.txt")

    def _run_compilation_test(self, tim_file: str, result_statements_file: str):
        # make sure to pass a resolved path to the tokenizer and ast generator
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / tim_file
        # tokenize the file to a stream
        tokens: Stream[Token] = Tokenizer(example_file).tokenize()
        # resolve the types in the file
        type_resolver: TypeResolver = TypeResolver(tokens)
        types: Types = type_resolver.resolve()
        # apply the types to the tokens in the stream
        type_applier: TypeApplier = TypeApplier(types)
        type_applier.apply(tokens)
        # generate the ast and resulting statements to verify
        ast: AST = AstGenerator(tokens).generate()
        ast_statements: list[Statement] = ast.statements.objects
        print(*ast_statements, sep="\n")

        # convert the individual statements to str to compare
        result_file: Path = this_folder / result_statements_file
        with open(result_file) as f:
            result: list[str] = f.readlines()
        # convert code lines to single lines and strip newlines
        code_lines: list[str] = []
        for statement in ast_statements:
            code_lines.extend(line.strip() for line in statement.c_code().split("\n"))
        # do the same for the result lines
        result_lines: list[str] = [line.strip() for line in result]
        # check that the lists are equal
        self.assertEqual(code_lines, result_lines)
