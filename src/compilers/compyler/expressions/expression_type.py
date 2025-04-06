#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from enum import auto
from enum import Enum


class ExpressionType(Enum):
    GROUPING = auto()
    MINUS = auto()
    NOT = auto()
