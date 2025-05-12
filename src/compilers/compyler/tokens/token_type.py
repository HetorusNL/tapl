#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

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
    INCREMENT = "++"
    DECREMENT = "--"

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
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    WHILE = "while"

    # special tokens
    INDENT = "<INDENT>"
    DEDENT = "<DEDENT"
    ERROR = "<ERROR>"
    NEWLINE = "<NEWLINE>"

    # combined variable declaration token
    VAR_DECL = "<VAR_DECL>"

    # end of file/input token
    EOF = "<EOF>"
