#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

import unittest
from typing import Any

from compyler.types.type import Type


class TestType(unittest.TestCase):
    def test_type_keyword(self):
        _type = Type("keyword")
        self.assertEqual(_type.keyword, "keyword")
        self.list_equal(_type.syntactic_sugar, [])
        self.list_equal(_type.all_keywords, ["keyword"])

    def test_type_syntactic_sugar_single(self):
        _type = Type("keyword", "sugar")
        self.assertEqual(_type.keyword, "keyword")
        self.list_equal(_type.syntactic_sugar, ["sugar"])
        self.list_equal(_type.all_keywords, ["keyword", "sugar"])

    def test_type_syntactic_sugar_multiple(self):
        _type = Type("kw", "sugar", "more", "third")
        self.assertEqual(_type.keyword, "kw")
        self.list_equal(_type.syntactic_sugar, ["sugar", "more", "third"])
        self.list_equal(_type.all_keywords, ["kw", "sugar", "more", "third"])

    def test_basic_type(self):
        _type1: Type = Type("test1", underlying_type="type")
        self.assertTrue(_type1.is_basic_type)
        self.assertEqual(_type1.underlying_type, "type")
        _type2: Type = Type("test2", "some", "sugar")
        self.assertFalse(_type2.is_basic_type)
        self.assertIsNone(_type2.underlying_type)

    def list_equal(self, left: list[Any], right: list[Any]):
        self.assertListEqual(sorted(left), sorted(right))
