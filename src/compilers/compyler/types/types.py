#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from pathlib import Path

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
            Type("u1", "bool", underlying_type="bool"),
            Type("u8", underlying_type="uint8_t"),
            Type("u16", underlying_type="uint16_t"),
            Type("u32", underlying_type="uint32_t"),
            Type("u64", underlying_type="uint64_t"),
            Type("s8", underlying_type="int8_t"),
            Type("s16", underlying_type="int16_t"),
            Type("s32", underlying_type="int32_t"),
            Type("s64", underlying_type="int64_t"),
            Type("f32", underlying_type="float"),
            Type("f64", underlying_type="double"),
            Type("string"),
        ]
        types: dict[str, Type] = {}
        for _type in self._types_list:
            for keyword in _type.all_keywords:
                assert keyword not in types
                types[keyword] = _type

        return types

    def add(self, keyword: str):
        """add a new type to the Types collection,
        does nothing when the type is already present in the collection
        """
        # check if the type is already in the collection
        if keyword in self._types:
            return
        # create the Type, and add the keyword:Type to the collection
        _type = Type(keyword)
        self._types[keyword] = _type

    def get(self, keyword: str) -> Type | None:
        """returns the Type with the provided keyword, None if not present"""
        return self._types.get(keyword)

    def generate_c_header(self, header_folder: Path) -> None:
        """generates a c types header for all builtin basic types in the header folder"""
        # add the strings to be added to the types header
        c_code: list[str] = [
            "#include <stdbool.h>\n",
            "#include <stdint.h>\n",
            "\n",
            "// typedefs for the builtin basic types defined in TAPL\n",
        ]

        # formulate the typedefs for the basic types used in TAPL
        for _type in self._types_list:
            if _type.is_basic_type:
                c_code.append(f"typedef {_type.underlying_type} {_type.keyword};\n")

        # write the content to the file
        types_header: Path = header_folder / "types.h"
        with open(types_header, "w") as f:
            f.writelines(c_code)
