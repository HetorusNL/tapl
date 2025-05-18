#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.


class Type:
    def __init__(self, keyword: str, *syntactic_sugar: str, underlying_type: str | None = None):
        self._keyword: str = keyword
        self._syntactic_sugar: list[str] = list(syntactic_sugar)
        self._underlying_type: str | None = underlying_type

    @property
    def keyword(self) -> str:
        """returns the keyword of the type"""
        return self._keyword

    @property
    def syntactic_sugar(self) -> list[str]:
        """returns the syntactic sugar list of the type"""
        return self._syntactic_sugar

    @property
    def all_keywords(self) -> list[str]:
        """returns, in any order, the keyword and syntactic sugars as list"""
        keywords: list[str] = [self.keyword]
        keywords.extend(self.syntactic_sugar)
        return keywords

    @property
    def is_basic_type(self) -> bool:
        """returns whether this is a basic type, that it has an underlying c-type"""
        return self.underlying_type is not None

    @property
    def underlying_type(self) -> str | None:
        """returns the underlying c-type, or None if it doesn't exist"""
        return self._underlying_type

    def non_void(self) -> bool:
        """returns whether the type is not of type void"""
        return self.keyword != "void"
