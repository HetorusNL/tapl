#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path
import unittest

from compyler.tokenizer import Tokenizer
from compyler.tokens.identifier_token import IdentifierToken
from compyler.tokens.token import Token
from compyler.tokens.var_decl_token import VarDeclToken
from compyler.types.type_applier import TypeApplier
from compyler.types.type_resolver import TypeResolver
from compyler.types.types import Types
from compyler.utils.stream import Stream


class TestTypeApplier(unittest.TestCase):
    def test_example_file(self):
        # first tokenize the file to get a list of tokens
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "example_type_applier.tim"
        tokenizer: Tokenizer = Tokenizer(example_file)
        tokens: Stream[Token] = tokenizer.tokenize()

        # then run the TypeResolver to get the custom types
        type_resolver: TypeResolver = TypeResolver(tokens)
        types: Types = type_resolver.resolve()

        # run the TypeApplier to create the VarDecl tokens
        type_applier: TypeApplier = TypeApplier(types)
        tokens = type_applier.apply(tokens)

        # extract the variable VarDecl tokens and values
        var_decl_tokens = [
            token for token in tokens.objects if isinstance(token, VarDeclToken)
        ]
        var_decl_values: list[str] = [token.name for token in var_decl_tokens]

        # check that all VarDecl tokens have been created
        # to ease testing, we only test if the variable name exists
        self.assertIn("byte", var_decl_values)
        self.assertIn("s", var_decl_values)
        self.assertIn("flag", var_decl_values)
        self.assertIn("instance", var_decl_values)
        self.assertIn("other_instance", var_decl_values)

        # extract the identifier tokens and their names
        identifier_tokens: list[IdentifierToken] = [
            token for token in tokens.objects if isinstance(token, IdentifierToken)
        ]
        identifier_values: list[str] = [token.value for token in identifier_tokens]

        # check that the type identifiers no longer exist in the token stream
        self.assertNotIn("u8", identifier_values)
        self.assertNotIn("string", identifier_values)
        self.assertNotIn("bool", identifier_values)
        # ClassName and OtherClass also exist in the declarations, so don't check

        # check that the variable names no longer exist in the token stream
        self.assertNotIn("byte", identifier_values)
        self.assertNotIn("s", identifier_values)
        self.assertNotIn("flag", identifier_values)
        self.assertNotIn("instance", identifier_values)
        self.assertNotIn("other_instance", identifier_values)
