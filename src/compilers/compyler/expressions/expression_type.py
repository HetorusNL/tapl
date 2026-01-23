#!/usr/bin/env python
#
# Copyright (c) 2026 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from enum import auto
from enum import Enum


class ExpressionType(Enum):
    GROUPING = auto()
    MINUS = auto()
    NOT = auto()
    POST_DECREMENT = auto()
    POST_INCREMENT = auto()
    PRE_DECREMENT = auto()
    PRE_INCREMENT = auto()
