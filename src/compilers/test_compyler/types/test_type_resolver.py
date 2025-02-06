from pathlib import Path
import unittest

from compyler.tokenizer import Tokenizer
from compyler.tokens import Token
from compyler.types import TypeResolver
from compyler.types import Types
from compyler.utils import Stream


class TestTypeResolver(unittest.TestCase):
    def test_example_file(self):
        # first tokenize the file to get a list of tokens
        this_folder: Path = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "example_type_resolver.tim"
        tokenizer: Tokenizer = Tokenizer(example_file)
        tokens: Stream[Token] = tokenizer.tokenize()

        # run the TypeResolver to get the types from the class-lines
        type_resolver: TypeResolver = TypeResolver(tokens)
        types: Types = type_resolver.resolve()

        # check that the classes exist in the resolver
        self.assertIsNotNone(types.get("ClassName"))
        self.assertIsNotNone(types.get("OtherClass"))
        # check that the last 'class' doesn't get in the types
        self.assertIsNone(types.get("class"))
