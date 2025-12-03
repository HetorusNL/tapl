#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.
#
# don't report this, as the unittests access private members:
# pyright: reportPrivateUsage=false

import unittest

from compyler.utils.stream import Stream
from compyler.utils.stream import StreamError


class TestStream(unittest.TestCase):
    def setUp(self):
        self.stream: Stream[int] = Stream()

    def test_objects(self):
        # add 5 objects and assert that these are in the internal list
        self.stream.add(1, 2, 3)
        self.assertListEqual([1, 2, 3], self.stream.objects)

    def test_adding_items(self):
        # initial test
        self.assertTrue(len(self.stream.objects) == 0)

        # test adding a value
        self.stream.add(1337)
        self.assertTrue(len(self.stream.objects) == 1)

        # test chained adding
        self.stream.add(2).add(3)
        self.assertTrue(len(self.stream.objects) == 3)

        # test adding multiple objects
        self.stream.add(4, 5, 6)
        self.assertListEqual([1337, 2, 3, 4, 5, 6], self.stream.objects)

    def test_iter(self):
        # add 5 objects to the stream
        self.stream.add(1, 2, 3, 4, 1337)

        # iterate the objects, while deleting every second entry
        objects: list[int] = []
        for i in self.stream.iter():
            objects.append(i)
            # not very neat way of causing the iterator to skip every second entry
            del self.stream.objects[0]

        # we should have element 1, 3, 5 of the iterator in objects now
        self.assertListEqual(objects, [1, 3, 1337])

    def test_iter_next(self):
        # empty stream raises exception
        with self.assertRaises(StreamError):
            self.stream.iter_next()

        # add 4 items to the stream
        self.stream.add(1, 2, 3, 4)

        # consume the first and let iter_next return the second till the fourth
        for value in self.stream.iter():
            self.assertEqual(value, 1)
            self.assertEqual(self.stream.iter_next(), 2)
            self.assertEqual(self.stream.iter_next(1), 3)
            self.assertEqual(self.stream.iter_next(2), 4)
            break

    def test_replace_negative_count(self):
        # populate the stream and start the iterator
        self.stream.add(1)
        list(self.stream.iter())

        # perform the checks
        with self.assertRaises(StreamError):
            self.stream.replace(-1, 1)
        with self.assertRaises(StreamError):
            self.stream.replace(-1337, 1)

    def test_replace_not_started_iterator(self):
        with self.assertRaises(StreamError):
            self.stream.replace(1, 1)

    def test_replace_index_too_high(self):
        # populate the stream with 2 objects, and set the index to 1 too high
        self.stream.add(1, 2)
        self.stream._index = len(self.stream.objects) + 2

        # perform the checks
        with self.assertRaises(StreamError):
            self.stream.replace(1, 1)

    def test_replace_single(self):
        # populate the stream with 3 objects, and run the iterator
        self.stream.add(1, 2, 3)
        list(self.stream.iter())

        # replace the last object
        self.assertEqual(3, self.stream.objects[self.stream._index - 1])
        self.stream.replace(1, 1337)
        self.assertEqual(1337, self.stream.objects[self.stream._index - 1])

        # replace the first object
        self.stream._index = 1
        self.assertEqual(1, self.stream.objects[self.stream._index - 1])
        self.stream.replace(1, 123)
        self.assertEqual(123, self.stream.objects[self.stream._index - 1])

        # replace the middle object
        self.stream._index = 2
        self.assertEqual(2, self.stream.objects[self.stream._index - 1])
        self.stream.replace(1, 10)
        self.assertEqual(10, self.stream.objects[self.stream._index - 1])

        # sanity check the whole iterator
        self.assertListEqual([123, 10, 1337], list(self.stream.iter()))

    def test_replace_zero(self):
        # populate the stream with 3 objects and set the iterator to point after 2
        self.stream.add(1, 2, 3)
        for value in self.stream.iter():
            if value == 2:
                self.stream.replace(0, 1337)
                break

        # perform the checks
        self.assertListEqual([1, 1337, 2, 3], self.stream.objects)

    def test_replace_some(self):
        # populate the list with 6 objects and set the iterator to point after 3
        self.stream.add(1, 2, 3, 4, 5, 6)
        for value in self.stream.iter():
            if value == 3:
                self.stream.replace(3, 1337)
                break

        # perform the checks
        self.assertListEqual([1, 2, 1337, 6], self.stream.objects)

    def test_replace_too_many(self):
        # populate the list with 6 objects and set the iterator to point after 3
        self.stream.add(1, 2, 3, 4, 5, 6)
        # try to replace 5 objects should fail
        for value in self.stream.iter():
            if value == 3:
                with self.assertRaises(StreamError):
                    self.stream.replace(5, 1337)

    def test_replace_till_the_end(self):
        # populate the list with 6 objects and set the iterator to point after 3
        self.stream.add(1, 2, 3, 4, 5, 6)
        # replace 4 values should still be good
        for value in self.stream.iter():
            if value == 3:
                self.stream.replace(4, 1337)

        # sanity check of the objects
        self.assertListEqual([1, 2, 1337], self.stream.objects)

    def test_stream_len(self):
        # empty stream has length of 0
        self.assertEqual(len(self.stream), 0)

        # add 2 objects, then the length should be 2
        self.stream.add(1, 2)
        self.assertEqual(len(self.stream), 2)

    def test_last(self):
        # initially the last should be None
        self.assertIsNone(self.stream.last())

        # adding objects should update the last function
        self.stream.add(1, 2)
        self.assertEqual(self.stream.last(), 2)
        self.stream.add(0)
        self.assertEqual(self.stream.last(), 0)

    def test_trueness(self):
        # empty stream should be False
        self.assertFalse(self.stream)

        # after adding objects, it should be True
        self.stream.add(0)
        self.assertTrue(self.stream)
