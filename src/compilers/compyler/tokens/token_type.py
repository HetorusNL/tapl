from enum import Enum


class TokenType(Enum):
    # single character tokens
    BRACE_CLOSE = "}"
    BRACE_OPEN = "{"
    BRACKET_CLOSE = "]"
    BRACKET_OPEN = "["
    COLON = ":"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PAREN_CLOSE = ")"
    PAREN_OPEN = "("
    PLUS = "+"
    SEMICOLON = ";"

    # single or double character tokens
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="
    NOT = "!"
    NOT_EQUAL = "!="
    SLASH = "/"
    STAR = "*"

    # literals
    IDENTIFIER = "<IDENTIFIER>"
    NUMBER = "<NUMBER>"
    STRING = "<STRING>"
    INLINE_COMMENT = "<INLINE_COMMENT>"
    BLOCK_COMMENT = "<BLOCK_COMMENT>"

    # keywords
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FOR = "for"
    IF = "if"
    NULL = "null"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    WHILE = "while"

    # special tokens
    INDENT = "<INDENT>"
    DEDENT = "<DEDENT"
    ERROR = "<ERROR>"

    # end of file/input token
    EOF = "<EOF>"
