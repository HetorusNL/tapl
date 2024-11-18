from pathlib import Path
import unittest

from compyler.tokenizer import Tokenizer
from compyler.token import Token


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        print()

    def test_tokenize_example(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "example.tim"
        tokens = Tokenizer(example_file).tokenize()
        print(tokens)

    def test_all_tokens(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "all_tokens.tim"
        tokens = Tokenizer(example_file).tokenize()
        all_tokens = [
            Token.BRACE_OPEN,
            Token.BRACE_CLOSE,
            Token.BRACKET_OPEN,
            Token.BRACKET_CLOSE,
            Token.COLON,
            Token.COMMA,
            Token.DOT,
            Token.MINUS,
            Token.PAREN_OPEN,
            Token.PAREN_CLOSE,
            Token.PLUS,
            Token.SEMICOLON,
            Token.INDENT,
            Token.EQUAL,
            Token.EQUAL_EQUAL,
            Token.GREATER,
            Token.GREATER_EQUAL,
            Token.LESS,
            Token.LESS_EQUAL,
            Token.NOT,
            Token.NOT_EQUAL,
            Token.SLASH,
            Token.SLASH_SLASH,
            Token.SLASH_STAR,
            Token.STAR,
            Token.STAR_SLASH,
            Token.INDENT,
            Token.IDENTIFIER,
            Token.NUMBER,
            Token.STRING,
            Token.DEDENT,
            Token.DEDENT,
            Token.CLASS,
            Token.ELSE,
            Token.FALSE,
            Token.FOR,
            Token.IF,
            Token.NULL,
            Token.RETURN,
            Token.SUPER,
            Token.THIS,
            Token.TRUE,
            Token.WHILE,
            Token.EOF,
        ]
        self.assertEqual(tokens, all_tokens)
