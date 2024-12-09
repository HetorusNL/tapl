from pathlib import Path

from .tokens.token_type import TokenType
from .tokens import CommentToken
from .tokens import IdentifierToken
from .tokens import NumberToken
from .tokens import StringToken
from .tokens import Token


class Tokenizer:
    INDENT_SPACES: int = 4

    def __init__(self, file: Path):
        print(f'tokenizing file: "{file}"')
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
                    self._add_token(TokenType.BRACE_CLOSE)
                case "{":
                    self._add_token(TokenType.BRACE_OPEN)
                case "]":
                    self._add_token(TokenType.BRACKET_CLOSE)
                case "[":
                    self._add_token(TokenType.BRACKET_OPEN)
                case ":":
                    self._add_token(TokenType.COLON)
                case ",":
                    self._add_token(TokenType.COMMA)
                case ".":
                    self._add_token(TokenType.DOT)
                case "-":
                    self._add_token(TokenType.MINUS)
                case ")":
                    self._add_token(TokenType.PAREN_CLOSE)
                case "(":
                    self._add_token(TokenType.PAREN_OPEN)
                case "+":
                    self._add_token(TokenType.PLUS)
                case ";":
                    self._add_token(TokenType.SEMICOLON)
                # match all single- or double-character tokens
                case "=":
                    if self._consume("="):
                        self._add_token(TokenType.EQUAL_EQUAL)
                    else:
                        self._add_token(TokenType.EQUAL)
                case ">":
                    if self._consume("="):
                        self._add_token(TokenType.GREATER_EQUAL)
                    else:
                        self._add_token(TokenType.GREATER)
                case "<":
                    if self._consume("="):
                        self._add_token(TokenType.LESS_EQUAL)
                    else:
                        self._add_token(TokenType.LESS)
                case "!":
                    if self._consume("="):
                        self._add_token(TokenType.NOT_EQUAL)
                    else:
                        self._add_token(TokenType.NOT)
                case "/":
                    if self._consume("/"):
                        self._add_inline_comment()
                    elif self._consume("*"):
                        self._add_block_comment()
                    else:
                        self._add_token(TokenType.SLASH)
                case "*":
                    self._add_token(TokenType.STAR)
                # match special EOF case, we parsed the whole file
                case None:
                    self._add_token(TokenType.EOF)
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
                    self._add_token(TokenType.ERROR)
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
        match: bool = self._get_char(consume=False) == char
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

    def _add_identifier_token(self, value: str) -> None:
        identifier_token: IdentifierToken = IdentifierToken(self._line, value)
        self._tokens.append(identifier_token)

    def _add_number_token(self, value: int) -> None:
        number_token: NumberToken = NumberToken(self._line, value)
        self._tokens.append(number_token)

    def _add_string_token(self, value: str) -> None:
        string_token: StringToken = StringToken(self._line, value)
        self._tokens.append(string_token)

    def _add_comment_token(self, token_type: TokenType, value: str) -> None:
        comment_token: CommentToken = CommentToken(token_type, self._line, value)
        self._tokens.append(comment_token)

    def _add_token(self, token_type: TokenType) -> None:
        token: Token = Token(token_type, self._line)
        self._tokens.append(token)

    def _add_number(self, first_char: str) -> None:
        # TODO: add 0b and 0x parsing
        # TODO: add distinction between int and float/double
        number_str: str = first_char
        while char := self._get_char(consume=False):
            # while we get digits, consume them and continue
            if self._isdigit(char):
                number_str += char
                self._current_index += 1
                continue
            break
        self._add_number_token(int(number_str))

    def _add_string(self) -> None:
        string: str = ""
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
            print(f'unterminated string "{string}"!')
            self._add_token(TokenType.ERROR)
            return
        self._add_string_token(string)

    def _add_keyword(self, identifier: str) -> bool:
        match identifier:
            case "class":
                self._add_token(TokenType.CLASS)
            case "else":
                self._add_token(TokenType.ELSE)
            case "false":
                self._add_token(TokenType.FALSE)
            case "for":
                self._add_token(TokenType.FOR)
            case "if":
                self._add_token(TokenType.IF)
            case "null":
                self._add_token(TokenType.NULL)
            case "return":
                self._add_token(TokenType.RETURN)
            case "super":
                self._add_token(TokenType.SUPER)
            case "this":
                self._add_token(TokenType.THIS)
            case "true":
                self._add_token(TokenType.TRUE)
            case "while":
                self._add_token(TokenType.WHILE)
            case _:
                # in de default case we haven't found a keyword
                return False
        # if we matched anything but the default case, we found a keyword
        return True

    def _add_inline_comment(self) -> None:
        comment_text = "//"
        while char := self._next():
            # while we get comment characters, consume them and continue
            if char == "\n":
                # restore the '\n', so the tokenizer can process it
                self._current_index -= 1
                break
            else:
                # add the character to the comment
                comment_text += char
        self._add_comment_token(TokenType.INLINE_COMMENT, comment_text)

    def _add_block_comment(self) -> None:
        comment_text = "/*"
        while char := self._next():
            # if we get an ending "*/", add the block comment token
            if char == "*" and self._consume("/"):
                comment_text += "*/"
                break
            else:
                # add the character to the comment
                comment_text += char
        else:
            # unterminated block comment
            print(f'unterminated block comment "{comment_text}"!')
            self._add_token(TokenType.ERROR)
            return
        self._add_comment_token(TokenType.BLOCK_COMMENT, comment_text)

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
        self._add_identifier_token(identifier)

    def _add_indent_dedent(self) -> None:
        spaces: int = 0
        while self._consume(" "):
            spaces += 1

        if spaces % self.INDENT_SPACES != 0:
            print(f"indentations must be a multiple of {self.INDENT_SPACES} spaces!")
            self._add_token(TokenType.ERROR)

        indent: int = spaces // self.INDENT_SPACES
        if indent > self._current_indent:
            # found one or more indentations
            for _ in range(indent - self._current_indent):
                self._add_token(TokenType.INDENT)
        elif indent < self._current_indent:
            # found one or more dedentations
            for _ in range(self._current_indent - indent):
                self._add_token(TokenType.DEDENT)

        # store the current amount of indentations
        self._current_indent: int = indent
