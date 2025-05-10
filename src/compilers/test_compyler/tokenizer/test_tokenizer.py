#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.
#
# don't report this, as the unittests access private members:
# pyright: reportPrivateUsage=false

from pathlib import Path
import unittest

from compyler.tokenizer import Tokenizer
from compyler.tokens.token_type import TokenType
from compyler.tokens.token import Token
from compyler.utils.stream import Stream


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        print()

    def test_tokenize_example(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "example.tim"
        tokenizer: Tokenizer = Tokenizer(example_file)
        token_stream: Stream[Token] = tokenizer.tokenize()
        tokens: list[Token] = token_stream.objects
        print(tokens)
        token_types: list[TokenType] = [token.token_type for token in tokens]
        # note that duplicate newlines and comments are discarded
        all_token_types = [
            TokenType.IF,
            TokenType.PAREN_OPEN,
            TokenType.TRUE,
            TokenType.PAREN_CLOSE,
            TokenType.COLON,
            TokenType.NEWLINE,
            TokenType.INDENT,
            TokenType.DEDENT,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.ERROR,
            TokenType.STRING,
            TokenType.NEWLINE,
            TokenType.ERROR,
            TokenType.NEWLINE,
            TokenType.ERROR,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.ERROR,
            TokenType.NEWLINE,
            TokenType.ERROR,
            TokenType.IDENTIFIER,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.IDENTIFIER,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.EOF,
        ]
        self.assertEqual(token_types, all_token_types)

        # also test the discarded tokens
        discarded_tokens: list[Token] = tokenizer._discarded_tokens.objects
        print(discarded_tokens)
        discarded_token_types: list[TokenType] = [token.token_type for token in discarded_tokens]
        all_discarded_token_types = [
            TokenType.INLINE_COMMENT,
            TokenType.NEWLINE,
            TokenType.NEWLINE,
            TokenType.INLINE_COMMENT,
            TokenType.NEWLINE,
            TokenType.INLINE_COMMENT,
            TokenType.NEWLINE,
            TokenType.NEWLINE,
            TokenType.INLINE_COMMENT,
            TokenType.NEWLINE,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
            TokenType.INLINE_COMMENT,
        ]
        self.assertEqual(discarded_token_types, all_discarded_token_types)

    def test_all_tokens(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "all_tokens.tim"
        tokenizer: Tokenizer = Tokenizer(example_file)
        token_stream: Stream[Token] = tokenizer.tokenize()
        tokens: list[Token] = token_stream.objects
        token_types: list[TokenType] = [token.token_type for token in tokens]
        all_token_types = [
            TokenType.BRACE_OPEN,
            TokenType.BRACE_CLOSE,
            TokenType.BRACKET_OPEN,
            TokenType.BRACKET_CLOSE,
            TokenType.COLON,
            TokenType.COMMA,
            TokenType.DOT,
            TokenType.MINUS,
            TokenType.PAREN_OPEN,
            TokenType.PAREN_CLOSE,
            TokenType.PLUS,
            TokenType.SEMICOLON,
            TokenType.NEWLINE,
            TokenType.INDENT,
            TokenType.EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.NOT,
            TokenType.NOT_EQUAL,
            TokenType.SLASH,
            TokenType.STAR,
            TokenType.NEWLINE,
            TokenType.INDENT,
            TokenType.IDENTIFIER,
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.NEWLINE,
            TokenType.DEDENT,
            TokenType.DEDENT,
            TokenType.CLASS,
            TokenType.ELSE,
            TokenType.FALSE,
            TokenType.FOR,
            TokenType.IF,
            TokenType.NULL,
            TokenType.PRINT,
            TokenType.RETURN,
            TokenType.SUPER,
            TokenType.THIS,
            TokenType.TRUE,
            TokenType.WHILE,
            TokenType.NEWLINE,
            TokenType.STRING,
            TokenType.NEWLINE,
            TokenType.NUMBER,
            TokenType.NEWLINE,
            TokenType.EOF,
        ]
        self.assertEqual(token_types, all_token_types)

        # also test the discarded tokens
        discarded_tokens: list[Token] = tokenizer._discarded_tokens.objects
        print(discarded_tokens)
        discarded_token_types: list[TokenType] = [token.token_type for token in discarded_tokens]
        all_discarded_token_types = [
            TokenType.INLINE_COMMENT,
            TokenType.NEWLINE,
            TokenType.BLOCK_COMMENT,
            TokenType.NEWLINE,
        ]
        self.assertEqual(discarded_token_types, all_discarded_token_types)
