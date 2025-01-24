from .type import Type


class Types:
    def __init__(self):
        self._types: dict[str, Type] = self.builtin_types()

    def builtin_types(self) -> dict[str, Type]:
        """returns the builtin types of the language as a dictionary:

        key: keyword
        value: Type"""
        types_list: list[Type] = [
            Type("u1", "bool"),
            Type("u8"),
            Type("u16"),
            Type("u32"),
            Type("u64"),
            Type("s8"),
            Type("s16"),
            Type("s32"),
            Type("s64"),
            Type("f32"),
            Type("f64"),
            Type("string"),
        ]
        types: dict[str, Type] = {}
        for _type in types_list:
            for keyword in _type.all_keywords:
                assert keyword not in types
                types[keyword] = _type

        return types

    def add(self, keyword: str):
        """add a new type to the Types collection,
        does nothing when the type is already present in the collection"""
        # check if the type is already in the collection
        if keyword in self._types:
            return
        # create the Type, and add the keyword:Type to the collection
        _type = Type(keyword)
        self._types[keyword] = _type

    def get(self, keyword: str) -> Type | None:
        """returns the Type with the provided keyword, None if not present"""
        return self._types.get(keyword)
