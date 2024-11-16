from pathlib import Path

from .token import Token


class Tokenizer:
    def __init__(self, file: Path):
        print(f"file: '{file}'")
        # for this compiler files will be small enough to load entirely into a string in memory
        with open(file) as f:
            self._file_characters: str = "".join(f.readlines())
        self._file_size = len(self._file_characters)
        # some variables to store the state of the tokenizer
        self._current_index: int = 0
        self._line = 1
        self._tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        # infinite loop until we reach the end of file
        while True:
            # switch-case for the next character
            match char := self._next():
                # match all single-character tokens
                case "}":
                    self._add_token(Token.BRACE_CLOSE)
                case "{":
                    self._add_token(Token.BRACE_OPEN)
                case "]":
                    self._add_token(Token.BRACKET_CLOSE)
                case "[":
                    self._add_token(Token.BRACKET_OPEN)
                case ",":
                    self._add_token(Token.COMMA)
                case ".":
                    self._add_token(Token.DOT)
                case "-":
                    self._add_token(Token.MINUS)
                case ")":
                    self._add_token(Token.PAREN_CLOSE)
                case "(":
                    self._add_token(Token.PAREN_OPEN)
                case "+":
                    self._add_token(Token.PLUS)
                case ";":
                    self._add_token(Token.SEMICOLON)
                # match all single- or double-character tokens
                case "=":
                    if self._consume("="):
                        self._add_token(Token.EQUAL_EQUAL)
                    else:
                        self._add_token(Token.EQUAL)
                case ">":
                    if self._consume("="):
                        self._add_token(Token.GREATER_EQUAL)
                    else:
                        self._add_token(Token.GREATER)
                case "<":
                    if self._consume("="):
                        self._add_token(Token.LESS_EQUAL)
                    else:
                        self._add_token(Token.LESS)
                case "!":
                    if self._consume("="):
                        self._add_token(Token.NOT_EQUAL)
                    else:
                        self._add_token(Token.NOT)
                case "/":
                    if self._consume("/"):
                        self._add_token(Token.SLASH_SLASH)
                    elif self._consume("*"):
                        self._add_token(Token.SLASH_STAR)
                    else:
                        self._add_token(Token.SLASH)
                case "*":
                    if self._consume("/"):
                        self._add_token(Token.STAR_SLASH)
                    else:
                        self._add_token(Token.STAR)
                # match special EOF case, we parsed the whole file
                case None:
                    self._add_token(Token.EOF)
                    break
                # match numbers and strings
                case digit if self._isdigit(char):
                    self._add_number(digit)
                case '"':
                    self._add_string()
                case alpha if self._isalpha(char):
                    self._add_identifier(alpha)
                # match whitespaces
                case " ":
                    pass
                case "\n":
                    self._line += 1
                case "\r":
                    # why use carriage return..
                    pass
                case "\t":
                    print("error: dammit, we use spaces not tabs!")
                case _:
                    print(f"unknown character '{char}', skipped...")
        return self._tokens

    def _next(self) -> str | None:
        """consume and return the next character in the file"""
        return self._get_char(consume=True)

    def _consume(self, character: str) -> bool:
        """check if the next character matches, consumes when matching"""
        # check that the next character matches the one providing
        match = self._get_char(consume=False) == character
        # if it's a match, consume it by incrementing the idex
        if match:
            self._current_index += 1
        # return whether it was a match
        return match

    def _get_char(self, consume) -> str | None:
        """utility function to combine _next and _consume"""
        # make sure to check the file size
        if self._current_index == self._file_size:
            return None
        # otherwise return the next character
        character: str = self._file_characters[self._current_index]
        if consume:
            self._current_index += 1
        return character

    def _isdigit(self, char: str) -> bool:
        return "0" <= char <= "9"

    def _isalpha(self, char: str) -> bool:
        return "a" <= char <= "z" or "A" <= char <= "Z" or char == "_"

    def _add_token(self, token: Token) -> None:
        self._tokens.append(token)

    def _add_number(self, first_char: str) -> None:
        number_str = first_char
        while char := self._get_char(consume=False):
            # while we get digits, consume them and continue
            if "0" <= char <= "9":
                number_str += char
                self._current_index += 1
                continue
            break
        print(f"parsed number '{int(number_str)}'")
        self._add_token(Token.NUMBER)

    def _add_string(self) -> None:
        string = ""
        while char := self._get_char(consume=False):
            # wait until we get a closing quote
            if char == '"':
                self._current_index += 1
                break
            # also handle the empty file case
            if char is None:
                print("unterminated string!")
                return
            # append to the string and consume the character
            string += char
            self._current_index += 1
        print(f"parsed string '{string}'")
        self._add_token(Token.STRING)

    def _add_identifier(self, first_alpha: str) -> None:
        string = first_alpha
        # TODO parse the identifier
        # TODO match keywords
        print(f"parsed identifier '{string}")
