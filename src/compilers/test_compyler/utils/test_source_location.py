#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

import unittest

from compyler.utils.source_location import SourceLocation


class TestSourceLocation(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(SourceLocation(1, 1), SourceLocation(1, 1))
        self.assertEqual(SourceLocation(1000, 0), SourceLocation(1000, 0))

    def test_not_equal(self):
        # test several source locations
        self.assertNotEqual(SourceLocation(1, 1), SourceLocation(2, 2))
        self.assertNotEqual(SourceLocation(10, 1), SourceLocation(10, 2))
        self.assertNotEqual(SourceLocation(1, 10), SourceLocation(2, 10))
        # test that other objects also aren't equal
        self.assertNotEqual(SourceLocation(1, 1), 1)
        self.assertNotEqual(SourceLocation(1, 1), 2)

    def test_add(self):
        # test side-by-side source locations
        location = SourceLocation(1, 3) + SourceLocation(4, 3)
        self.assertEqual(location.start, 1)
        self.assertEqual(location.length, 6)
        # test source locations with space between them
        location = SourceLocation(2, 3) + SourceLocation(10, 3)
        self.assertEqual(location.start, 2)
        self.assertEqual(location.length, 11)
        # test overlapping source locations
        location = SourceLocation(2, 3) + SourceLocation(1, 3)
        self.assertEqual(location.start, 1)
        self.assertEqual(location.length, 4)
