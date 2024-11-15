from pathlib import Path

from .token import Token


class Tokenizer:
    def __init__(self, file: Path):
        print(f"file: '{file}'")
        # for this compiler files will be small enough to load entirely into a string in memory
        with open(file) as f:
            self.file_characters: str = "".join(f.readlines())
        self.file_size = len(self.file_characters)
        # some variables to store the state of the tokenizer
        self.current_index: int = 0
        self.line = 1
        self.tokens: list[Token] = []

    def tokenize(self):
        # infinite loop until we reach the end of file
        while True:
            # switch-case for the next character
            match self._next():
                # match all single-character tokens
                case "]":
                    self._add_token(Token.BRACKET_CLOSE)
                case "[":
                    self._add_token(Token.BRACKET_OPEN)
                case ")":
                    self._add_token(Token.PAREN_CLOSE)
                case "(":
                    self._add_token(Token.PAREN_OPEN)
                case "+":
                    self._add_token(Token.PLUS)
                case "!":
                    self._add_token(Token.NOT)
                # match newline
                case "\n":
                    self.line += 1
                case _ as default:
                    if default is None:
                        # parsed the whole file, generate an EOF token
                        self._add_token(Token.EOF)
                        break
                    print(f"unknown character '{default}', skipped...")
        return self.tokens

    def _next(self) -> str | None:
        """return the next token in the file"""
        # make sure to check the file size
        if self.current_index == self.file_size:
            return None
        # otherwise return the next character and increment current_index
        character: str = self.file_characters[self.current_index]
        self.current_index += 1
        return character

    def _add_token(self, token: Token):
        self.tokens.append(token)
