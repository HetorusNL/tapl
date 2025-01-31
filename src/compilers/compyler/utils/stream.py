from collections.abc import Iterator


class StreamError(ValueError):
    def __init__(self, *args: object):
        super().__init__(args)


class Stream[T]:
    """encapsulates a stream of objects.

    objects can be appended to the stream.
    there is an iterator over the objects in the stream.
    objects in the iterator can be replaced with other objects.
    while the iterator is running, objects can be added or replaced."""

    def __init__(self):
        self._objects: list[T] = []
        self._index: int = 0

    def add(self, *objs: T) -> "Stream[T]":
        """extend the stream with the objects provided"""
        self._objects.extend(objs)
        return self

    def iter(self) -> Iterator[T]:
        """returns an iterator over the stream.

        note that the internal state of the iterators from this function are shared!"""
        self._index = 0
        while self._index < len(self._objects):
            self._index += 1
            yield self._objects[self._index - 1]

    def replace(self, count: int, replacement: T) -> None:
        """replaces [count] objects with [replacement].
        starting from the element last returned by the call to next"""
        # negative count values are not possible
        if count < 0:
            raise StreamError("can't replace negative amount of objects!")

        # sanity check the instance's index
        if self._index == 0:
            raise StreamError("invalid state of the iterator!")
        if self._index > len(self._objects) + 1:
            raise StreamError("iterator is outside of stream's objects!")

        # speed up the edge case where count is 1, replace the object
        if count == 1:
            self._objects[self._index - 1] = replacement
            return

        # other cases, delete count objects (when nonzero count)
        if count != 0:
            # check that we can delete count objects
            if self._index + count - 1 > len(self._objects):
                raise StreamError("can't replace this many objects")
            # success, delete the objects
            del self._objects[self._index - 1 : self._index - 1 + count]
        # and add replacement
        self._objects.insert(self._index - 1, replacement)
