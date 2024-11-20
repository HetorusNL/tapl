from pathlib import Path
import unittest

from compyler.token_type import TokenType
from compyler.tokenizer import Tokenizer
from compyler.tokens import Token


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        print()

    def test_tokenize_example(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "example.tim"
        tokens: list[Token] = Tokenizer(example_file).tokenize()
        print(tokens)

    def test_all_tokens(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "all_tokens.tim"
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
            TokenType.SLASH_SLASH,
            TokenType.SLASH_STAR,
            TokenType.STAR,
            TokenType.STAR_SLASH,
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
            TokenType.EOF,
        ]
        self.assertEqual(token_types, all_token_types)
