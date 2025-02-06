from pathlib import Path

from .tokens.token_type import TokenType
from .tokens import CommentToken
from .tokens import IdentifierToken
from .tokens import NumberToken
from .tokens import StringToken
from .tokens import Token
from .utils import Stream


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
        self._tokens: Stream[Token] = Stream()

    def tokenize(self) -> Stream[Token]:
        """tokenize the file and return a token stream"""
        # infinite loop until we reach the end of file
        while True:
            # process indent/dedent from spaces at start of line
            if self._at_start_of_line:
                self._add_indent_dedent()

            # switch-case for the next character
            match char := self._next():
                # match all single-character tokens
                case TokenType.BRACE_CLOSE.value:
                    self._add_token(TokenType.BRACE_CLOSE)
                case TokenType.BRACE_OPEN.value:
                    self._add_token(TokenType.BRACE_OPEN)
                case TokenType.BRACKET_CLOSE.value:
                    self._add_token(TokenType.BRACKET_CLOSE)
                case TokenType.BRACKET_OPEN.value:
                    self._add_token(TokenType.BRACKET_OPEN)
                case TokenType.COLON.value:
                    self._add_token(TokenType.COLON)
                case TokenType.COMMA.value:
                    self._add_token(TokenType.COMMA)
                case TokenType.DOT.value:
                    self._add_token(TokenType.DOT)
                case TokenType.MINUS.value:
                    self._add_token(TokenType.MINUS)
                case TokenType.PAREN_CLOSE.value:
                    self._add_token(TokenType.PAREN_CLOSE)
                case TokenType.PAREN_OPEN.value:
                    self._add_token(TokenType.PAREN_OPEN)
                case TokenType.PLUS.value:
                    self._add_token(TokenType.PLUS)
                case TokenType.SEMICOLON.value:
                    self._add_token(TokenType.SEMICOLON)
                # match all single- or double-character tokens
                case TokenType.EQUAL.value:
                    if self._consume(TokenType.EQUAL.value):
                        self._add_token(TokenType.EQUAL_EQUAL)
                    else:
                        self._add_token(TokenType.EQUAL)
                case TokenType.GREATER.value:
                    if self._consume(TokenType.EQUAL.value):
                        self._add_token(TokenType.GREATER_EQUAL)
                    else:
                        self._add_token(TokenType.GREATER)
                case TokenType.LESS.value:
                    if self._consume(TokenType.EQUAL.value):
                        self._add_token(TokenType.LESS_EQUAL)
                    else:
                        self._add_token(TokenType.LESS)
                case TokenType.NOT.value:
                    if self._consume(TokenType.EQUAL.value):
                        self._add_token(TokenType.NOT_EQUAL)
                    else:
                        self._add_token(TokenType.NOT)
                case TokenType.SLASH.value:
                    if self._consume(TokenType.SLASH.value):
                        self._add_inline_comment()
                    elif self._consume(TokenType.STAR.value):
                        self._add_block_comment()
                    else:
                        self._add_token(TokenType.SLASH)
                case TokenType.STAR.value:
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
                    self._add_token(TokenType.NEWLINE)
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

    def _isbinary(self, char: str) -> bool:
        return "0" <= char <= "1"

    def _isdigit(self, char: str) -> bool:
        return "0" <= char <= "9"

    def _ishex(self, char: str) -> bool:
        return self._isdigit(char) or "a" <= char.lower() <= "f"

    def _isalpha(self, char: str) -> bool:
        return "a" <= char <= "z" or "A" <= char <= "Z"

    def _is_identifier_char(self, char: str) -> bool:
        return self._isdigit(char) or self._isalpha(char) or char == "_"

    def _add_identifier_token(self, value: str) -> None:
        identifier_token: IdentifierToken = IdentifierToken(self._line, value)
        self._tokens.add(identifier_token)

    def _add_number_token(self, value: int) -> None:
        number_token: NumberToken = NumberToken(self._line, value)
        self._tokens.add(number_token)

    def _add_string_token(self, value: str) -> None:
        string_token: StringToken = StringToken(self._line, value)
        self._tokens.add(string_token)

    def _add_comment_token(self, token_type: TokenType, value: str) -> None:
        comment_token: CommentToken = CommentToken(token_type, self._line, value)
        self._tokens.add(comment_token)

    def _add_token(self, token_type: TokenType) -> None:
        token: Token = Token(token_type, self._line)
        self._tokens.add(token)

    def _add_binary_number(self) -> None:
        """parse a binary number starting with 0b, or an error token if invalid"""
        binary_str: str = "0b"
        self._current_index += 1
        while char := self._get_char(consume=False):
            if self._isbinary(char):
                binary_str += char
                self._current_index += 1
                continue
            break
        if len(binary_str) == 2:
            print(f'invalid binary value "{binary_str}"!')
            self._add_token(TokenType.ERROR)
        else:
            self._add_number_token(int(binary_str, 2))

    def _add_hexadecimal_number(self) -> None:
        """parse a hexadecimal number starting with 0x, or an error token if invalid"""
        hexadecimal_str: str = "0x"
        self._current_index += 1
        while char := self._get_char(consume=False):
            if self._ishex(char):
                hexadecimal_str += char
                self._current_index += 1
                continue
            break
        if len(hexadecimal_str) == 2:
            print(f'invalid hexadecimal value "{hexadecimal_str}"!')
            self._add_token(TokenType.ERROR)
        else:
            self._add_number_token(int(hexadecimal_str, 16))

    def _add_number(self, first_char: str) -> None:
        # TODO: add distinction between int and float/double
        # TODO: add e numbers, e.g. 1e3, for int and float/double
        # differentiate between binary, hexadecimal, 0-prefixed and normal numbers
        if first_char == "0":
            match char := self._get_char(consume=False):
                case "b":
                    return self._add_binary_number()
                case "x":
                    return self._add_hexadecimal_number()
                case None:
                    # EOF, the file ends with number '0'
                    return self._add_number_token(0)
                case _ if self._isdigit(char):
                    # ordinary number prefixed with a '0', parse below
                    pass
                case _:
                    # the value '0'
                    return self._add_number_token(0)

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
            case TokenType.CLASS.value:
                self._add_token(TokenType.CLASS)
            case TokenType.ELSE.value:
                self._add_token(TokenType.ELSE)
            case TokenType.FALSE.value:
                self._add_token(TokenType.FALSE)
            case TokenType.FOR.value:
                self._add_token(TokenType.FOR)
            case TokenType.IF.value:
                self._add_token(TokenType.IF)
            case TokenType.NULL.value:
                self._add_token(TokenType.NULL)
            case TokenType.RETURN.value:
                self._add_token(TokenType.RETURN)
            case TokenType.SUPER.value:
                self._add_token(TokenType.SUPER)
            case TokenType.THIS.value:
                self._add_token(TokenType.THIS)
            case TokenType.TRUE.value:
                self._add_token(TokenType.TRUE)
            case TokenType.WHILE.value:
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
                # increment line number here
                self._line += 1
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
