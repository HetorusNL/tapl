# don't report this, as the unittests access private members
# pyright: reportPrivateUsage=false

import unittest

from compyler.types import Type
from compyler.types import Types


class TestTypes(unittest.TestCase):
    def test_builtin_types(self):
        types: Types = Types()

        # test that the keyword and sugar objects point to same type
        self.assertEqual(types._types["u1"], types._types["bool"])

        # test that other types are different
        self.assertNotEqual(types._types["u1"], types._types["u8"])

    def test_add_existing_type(self):
        # test that adding existing type doesn't add it
        types: Types = Types()
        # extract the first keyword
        types_keys = types._types.keys()
        keyword: str = list(types_keys)[0]
        num_keys_before: int = len(types._types.keys())
        types.add(keyword)
        num_keys_after: int = len(types._types.keys())
        self.assertEqual(num_keys_before, num_keys_after)

    def test_add_new_type(self):
        # test that a new type is added, and points to the same type
        types: Types = Types()
        types.add("non_existing_type_1337")
        self.assertTrue(types._types.get("non_existing_type_1337"))

    def test_get_nonexisting_type(self):
        # test that None is returned when a type doesn't exist
        types: Types = Types()
        self.assertIsNone(types.get("non_existing_type_1337"))

    def test_get_builtin_type(self):
        # test that builtin types can also be getted
        types: Types = Types()
        self.assertIsInstance(types.get("u1"), Type)

    def test_get_added_type(self):
        # test that a type added, can be getted
        types: Types = Types()
        types.add("new_type_1337")
        self.assertIsInstance(types.get("new_type_1337"), Type)
