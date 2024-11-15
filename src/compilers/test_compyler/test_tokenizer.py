from pathlib import Path
import unittest

from compyler.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    def test_tokenize_example(self):
        # make sure to pass a resolved path to the tokenizer
        this_folder = Path(__file__).parent.resolve()
        example_file: Path = this_folder / "example.tim"
        tokens = Tokenizer(example_file).tokenize()
        print(tokens)
