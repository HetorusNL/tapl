#!/usr/bin/env python
#
# Copyright (c) 2026 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.


class TaplError(BaseException):
    def __init__(self, message: str):
        super().__init__(message)
