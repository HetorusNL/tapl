from enum import Enum
from enum import auto


class Token(Enum):
    # single character tokens
    BRACE_CLOSE = auto()
    BRACE_OPEN = auto()
    BRACKET_CLOSE = auto()
    BRACKET_OPEN = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PAREN_CLOSE = auto()
    PAREN_OPEN = auto()
    PLUS = auto()
    SEMICOLON = auto()
    STAR = auto()

    # single or double character tokens
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    NOT = auto()
    NOT_EQUAL = auto()
    SLASH = auto()
    SLASH_SLASH = auto()
    SLASH_STAR = auto()

    # literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # keywords
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FOR = auto()
    NULL = auto()
    OR = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    WHILE = auto()

    # end of file/input token
    EOF = auto()
