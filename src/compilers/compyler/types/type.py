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
        self._promotions: list[Type] = []

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

    def add_promotions(self, *promotions: "Type") -> None:
        """add promotions to which this type can promote to"""
        self._promotions.extend(promotions)

    def get_promotions(self) -> list["Type"]:
        """get the list of promotions of this type"""
        return self._promotions

    def can_promote_to(self, other: "Type") -> bool:
        """check if this type can be promoted (or is of same type) as other"""
        return other == self or other in self.get_promotions()

    def non_void(self) -> bool:
        """returns whether the type is not of type void"""
        return self.keyword != "void"

    def __eq__(self, other: object) -> bool:
        """two types are equal when they have the same keyword"""
        if type(other) != Type:
            return False

        return self.keyword == other.keyword
