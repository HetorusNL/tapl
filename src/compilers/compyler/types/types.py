#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

from .numeric_type import NumericType
from .type import Type


class Types:
    def __init__(self):
        self._types: dict[str, Type] = self.builtin_types()

    def builtin_types(self) -> dict[str, Type]:
        """returns the builtin types of the language as a dictionary:

        key: keyword
        value: Type
        """
        # also store the list of types in the class
        self._types_list: list[Type] = [
            Type("void", underlying_type="void"),
            NumericType("u1", "bool", underlying_type="bool"),
            NumericType("u8", underlying_type="uint8_t"),
            NumericType("u16", underlying_type="uint16_t"),
            NumericType("u32", underlying_type="uint32_t"),
            NumericType("u64", underlying_type="uint64_t"),
            NumericType("s8", underlying_type="int8_t"),
            NumericType("s16", underlying_type="int16_t"),
            NumericType("s32", underlying_type="int32_t"),
            NumericType("s64", underlying_type="int64_t"),
            NumericType("f32", underlying_type="float"),
            NumericType("f64", underlying_type="double"),
            Type("string"),
        ]
        types: dict[str, Type] = {}
        for type_ in self._types_list:
            for keyword in type_.all_keywords:
                assert keyword not in types
                types[keyword] = type_

        # add the promotions for the basic types
        u1: Type = types["u1"]
        assert type(u1) == NumericType
        u1.add_promotions(types["u8"], types["u16"], types["u32"], types["u64"])
        u8: Type = types["u8"]
        assert type(u8) == NumericType
        u8.add_promotions(types["u16"], types["u32"], types["u64"])
        u16: Type = types["u16"]
        assert type(u16) == NumericType
        u16.add_promotions(types["u32"], types["u64"])
        u32: Type = types["u32"]
        assert type(u32) == NumericType
        u32.add_promotions(types["u64"])
        s8: Type = types["s8"]
        assert type(s8) == NumericType
        s8.add_promotions(types["s16"], types["s32"], types["s64"])
        s16: Type = types["s16"]
        assert type(s16) == NumericType
        s16.add_promotions(types["s32"], types["s64"])
        s32: Type = types["s32"]
        assert type(s32) == NumericType
        s32.add_promotions(types["s64"])
        f32: Type = types["f32"]
        assert type(f32) == NumericType
        f32.add_promotions(types["f64"])

        return types

    def add(self, keyword: str):
        """add a new type to the Types collection,
        does nothing when the type is already present in the collection
        """
        # check if the type is already in the collection
        if keyword in self._types:
            return
        # create the Type, and add the keyword:Type to the collection
        type_ = Type(keyword)
        self._types[keyword] = type_

    def get(self, keyword: str) -> Type | None:
        """returns the Type with the provided keyword, None if not present"""
        return self._types.get(keyword)

    def generate_c_header(self, header_folder: Path) -> None:
        """generates a c types header for all builtin basic types in the header folder"""
        # add the strings to be added to the types header
        c_code: list[str] = [
            "#pragma once\n",
            "\n",
            "#include <stdbool.h>\n",
            "#include <stdint.h>\n",
            "\n",
            "// typedefs for the builtin basic types defined in TAPL\n",
        ]

        # formulate the typedefs for the basic types used in TAPL
        for type_ in self._types_list:
            if type_.is_basic_type:
                # only add the type if it has a different name in c
                if type_.underlying_type != type_.keyword:
                    c_code.append(f"typedef {type_.underlying_type} {type_.keyword};\n")

        # write the content to the file
        types_header: Path = header_folder / "types.h"
        with open(types_header, "w") as f:
            f.writelines(c_code)
