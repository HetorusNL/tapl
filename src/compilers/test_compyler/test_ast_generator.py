from pathlib import Path
import unittest

from compyler.ast import AST
from compyler.ast_generator import AstGenerator
from compyler.expressions import BinaryExpression
from compyler.expressions import TokenExpression
from compyler.expressions import UnaryExpression
from compyler.expressions.expression_type import ExpressionType
from compyler.tokenizer import Tokenizer
from compyler.tokens import Token
from compyler.tokens import NumberToken
from compyler.tokens.token_type import TokenType


class TestAstGenerator(unittest.TestCase):
    def setUp(self):
        print()

    def test_ast_generator_example(self):
        # make sure to pass a resolved path to the tokenizer and ast generator
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "ast_generator" / "example.tim"
        tokens: list[Token] = Tokenizer(example_file).tokenize()
        ast: AST = AstGenerator(tokens).generate()
        ast_result = [
            BinaryExpression(
                BinaryExpression(
                    BinaryExpression(
                        TokenExpression(NumberToken(1, 1100)),
                        Token(TokenType.PLUS, 1),
                        BinaryExpression(
                            TokenExpression(NumberToken(1, 150)),
                            Token(TokenType.STAR, 1),
                            TokenExpression(NumberToken(1, 2)),
                        ),
                    ),
                    Token(TokenType.PLUS, 1),
                    TokenExpression(NumberToken(1, 37)),
                ),
                Token(TokenType.MINUS, 1),
                TokenExpression(NumberToken(1, 100)),
            ),
            BinaryExpression(
                BinaryExpression(
                    TokenExpression(NumberToken(2, 1)),
                    Token(TokenType.STAR, 2),
                    TokenExpression(NumberToken(2, 2)),
                ),
                Token(TokenType.PLUS, 2),
                BinaryExpression(
                    TokenExpression(NumberToken(2, 3)),
                    Token(TokenType.SLASH, 2),
                    UnaryExpression(
                        ExpressionType.GROUPING,
                        BinaryExpression(
                            TokenExpression(NumberToken(2, 4)),
                            Token(TokenType.PLUS, 2),
                            TokenExpression(Token(TokenType.TRUE, 2)),
                        ),
                    ),
                ),
            ),
        ]
        print(*ast.expressions, sep="\n")
        self.assertEqual(str(ast.expressions), str(ast_result))

        # or simpler converting the individual expressions to str
        result = [
            "(((1100 + (150 * 2)) + 37) - 100)",
            "((1 * 2) + (3 / ((4 + true))))",
        ]
        self.assertEqual(
            [expression.c_code() for expression in ast.expressions], result
        )
