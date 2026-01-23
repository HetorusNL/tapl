#!/usr/bin/env python
#
# Copyright (c) 2026 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from enum import auto
from enum import Enum


class NumericTypeType(Enum):
    SIGNED = auto()
    UNSIGNED = auto()
    FLOATING_POINT = auto()
