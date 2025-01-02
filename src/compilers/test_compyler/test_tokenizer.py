from pathlib import Path
import unittest

from compyler.tokenizer import Tokenizer
from compyler.tokens.token_type import TokenType
from compyler.tokens import Token


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        print()

    def test_tokenize_example(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "tokenizer" / "example.tim"
        tokens: list[Token] = Tokenizer(example_file).tokenize()
        print(tokens)
        token_types: list[TokenType] = [token.token_type for token in tokens]
        all_token_types = [
            TokenType.IF,
            TokenType.PAREN_OPEN,
            TokenType.TRUE,
            TokenType.PAREN_CLOSE,
            TokenType.COLON,
            TokenType.INDENT,
            TokenType.INLINE_COMMENT,
            TokenType.DEDENT,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.ERROR,
            TokenType.STRING,
            TokenType.INLINE_COMMENT,
            TokenType.ERROR,
            TokenType.INLINE_COMMENT,
            TokenType.ERROR,
            TokenType.NUMBER,
            TokenType.INLINE_COMMENT,
            TokenType.ERROR,
            TokenType.INLINE_COMMENT,
            TokenType.ERROR,
            TokenType.IDENTIFIER,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.IDENTIFIER,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.INLINE_COMMENT,
            TokenType.NUMBER,
            TokenType.EOF,
        ]
        self.assertEqual(token_types, all_token_types)

    def test_all_tokens(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "tokenizer" / "all_tokens.tim"
        tokens: list[Token] = Tokenizer(example_file).tokenize()
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
            TokenType.INDENT,
            TokenType.IDENTIFIER,
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.DEDENT,
            TokenType.DEDENT,
            TokenType.CLASS,
            TokenType.ELSE,
            TokenType.FALSE,
            TokenType.FOR,
            TokenType.IF,
            TokenType.NULL,
            TokenType.RETURN,
            TokenType.SUPER,
            TokenType.THIS,
            TokenType.TRUE,
            TokenType.WHILE,
            TokenType.INLINE_COMMENT,
            TokenType.STRING,
            TokenType.BLOCK_COMMENT,
            TokenType.NUMBER,
            TokenType.EOF,
        ]
        self.assertEqual(token_types, all_token_types)
