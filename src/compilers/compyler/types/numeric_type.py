#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from .type import Type


class NumericType(Type):
    def __init__(self, keyword: str, *syntactic_sugar: str, underlying_type: str | None = None):
        super().__init__(keyword, *syntactic_sugar, underlying_type=underlying_type)
        self._promotions: list[Type] = []

    def add_promotions(self, *promotions: "Type") -> None:
        """add promotions to which this type can promote to"""
        self._promotions.extend(promotions)

    def get_promotions(self) -> list["Type"]:
        """get the list of promotions of this type"""
        return self._promotions

    def can_promote_to(self, other: "Type") -> bool:
        """check if this type can be promoted (or is of same type) as other"""
        return other == self or other in self.get_promotions()
