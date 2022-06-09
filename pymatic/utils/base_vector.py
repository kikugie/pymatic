from abc import ABC, abstractmethod


class BaseVector(tuple, ABC):
    def _add(self, other):
        return [i + j for i, j in zip(self, other)]

    def __add__(self, other):
        return self.__class__(self._add(other))

    def __iadd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return self.__class__([-i for i in self])

    def __sub__(self, other):
        return self.__class__(self._add(-other))

    def __isub__(self, other):
        return self.__sub__(other)

    def __abs__(self):
        return self.__class__([abs(i) for i in self])

    @classmethod
    def from_list(cls, lst: list | tuple, /) -> 'BaseVector':
        return cls(*lst)

    @classmethod
    @abstractmethod
    def from_unsafe_dict(cls, dct: dict, /) -> 'BaseVector':
        """
        Handles the case when dict has more values than the vector should have.
        """
        ...
