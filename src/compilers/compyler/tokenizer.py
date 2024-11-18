from pathlib import Path

from .token import Token


class Tokenizer:
    INDENT_SPACES: int = 4

    def __init__(self, file: Path):
        print(f"tokenizing file: '{file}'")
        # for this compiler files will be small enough to load entirely into a string in memory
        with open(file) as f:
            self._file_characters: str = "".join(f.readlines())
        self._file_size: int = len(self._file_characters)

        # some variables to store the state of the tokenizer
        self._current_index: int = 0
        self._line: int = 1
        # indent and dedent related variables
        self._at_start_of_line: bool = True
        self._current_indent: int = 0  # current number of INDENT_SPACES indentations
        # the resulting tokens from the tokenizer
        self._tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        # infinite loop until we reach the end of file
        while True:
            # process indent/dedent from spaces at start of line
            if self._at_start_of_line:
                self._add_indent_dedent()

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
                case ":":
                    self._add_token(Token.COLON)
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
                    # first match a digit, as identifiers can't start with a digit
                    self._add_number(digit)
                case '"':
                    self._add_string()
                case identifier_char if self._is_identifier_char(char):
                    self._add_identifier(identifier_char)
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
                    self._add_token(Token.ERROR)
                case _:
                    print(f"unknown character '{char}', skipped...")
            # after \n we're at start of line, we can expect indent/dedent here
            self._at_start_of_line = char == "\n"
        return self._tokens

    def _next(self) -> str | None:
        """consume and return the next character in the file"""
        return self._get_char(consume=True)

    def _consume(self, char: str) -> bool:
        """check if the next character matches, consumes when matching"""
        # check that the next character matches the one providing
        match = self._get_char(consume=False) == char
        # if it's a match, consume it by incrementing the idex
        if match:
            self._current_index += 1
        # return whether it was a match
        return match

    def _get_char(self, consume: bool) -> str | None:
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
        return "a" <= char <= "z" or "A" <= char <= "Z"

    def _is_identifier_char(self, char: str) -> bool:
        return self._isdigit(char) or self._isalpha(char) or char == "_"

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
            # append to the string and consume the character
            string += char
            self._current_index += 1
        # also handle the empty file case
        if char is None:
            print(f"unterminated string '\"{string}'!")
            self._add_token(Token.ERROR)
            return
        print(f"parsed string '{string}'")
        self._add_token(Token.STRING)

    def _add_keyword(self, identifier: str) -> bool:
        match identifier:
            case "class":
                self._add_token(Token.CLASS)
            case "else":
                self._add_token(Token.ELSE)
            case "false":
                self._add_token(Token.FALSE)
            case "for":
                self._add_token(Token.FOR)
            case "if":
                self._add_token(Token.IF)
            case "null":
                self._add_token(Token.NULL)
            case "return":
                self._add_token(Token.RETURN)
            case "super":
                self._add_token(Token.SUPER)
            case "this":
                self._add_token(Token.THIS)
            case "true":
                self._add_token(Token.TRUE)
            case "while":
                self._add_token(Token.WHILE)
            case _:
                # in de default case we haven't found a keyword
                return False
        # if we matched anything but the default case, we found a keyword
        return True

    def _add_identifier(self, first_alpha: str) -> None:
        identifier = first_alpha
        while char := self._get_char(consume=False):
            # while we get identifier characters, consume them and continue
            if self._is_identifier_char(char):
                identifier += char
                self._current_index += 1
                continue
            break

        # match keywords, and return if the identifier is a keyword
        if self._add_keyword(identifier):
            return

        # otherwise we have found an identifier
        print(f"parsed identifier '{identifier}'")
        self._add_token(Token.IDENTIFIER)

    def _add_indent_dedent(self) -> None:
        spaces: int = 0
        while self._consume(" "):
            spaces += 1

        if spaces % self.INDENT_SPACES != 0:
            print(f"indentations must be a multiple of {self.INDENT_SPACES} spaces!")
            self._add_token(Token.ERROR)

        indent: int = spaces // self.INDENT_SPACES
        if indent > self._current_indent:
            # found one or more indentations
            for _ in range(indent - self._current_indent):
                self._add_token(Token.INDENT)
        elif indent < self._current_indent:
            # found one or more dedentations
            for _ in range(self._current_indent - indent):
                self._add_token(Token.DEDENT)

        # store the current amount of indentations
        self._current_indent = indent
