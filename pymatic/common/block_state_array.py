from abc import ABC, abstractmethod

from attrs import define
from nbtlib import Array

from pymatic.common.block_state import BlockState
from pymatic.common.nbt_object import NBTObject


@define(kw_only=True)
class BlockStateArray(NBTObject, ABC):
    block_states: list | Array
    palette: list
    length: int  # amount of encoded block states

    # @classmethod
    # @abstractmethod
    # def new(cls, size: int, bit_span: int):
    #     ...
    # TODO this

    @abstractmethod
    def get(self, index: int, /) -> int | list:
        ...

    @abstractmethod
    def set(self, index: int, value: int, /):
        ...

    @abstractmethod
    def update(self):
        ...

    def block_iterator(self, iter_range: range = None, /):
        # TODO: Write iteration algorithm
        if iter_range is None:
            iter_range = range(self.length)
        for i in iter_range:
            yield self[i]

    def __setitem__(self, key: int | slice, value: int):
        if isinstance(key, int) and self.__key_check(key):
            self.set(key, value) if key >= 0 else self.set(self.length + key, value)
            return
        for k in range(self.length)[key]:
            self[k] = value

    def __getitem__(self, key: int | slice) -> int | list:
        if isinstance(key, int) and self.__key_check(key):
            return self.get(key) if key >= 0 else self.get(self.length + key)
        return [self[k] for k in range(self.length)[key]]

    def __iter__(self):
        for i in range(self.length):
            yield BlockStateLink(self, i)

    def __delitem__(self, key: int):
        self[key] = 0

    def __contains__(self, value: int):
        for i in self.block_iterator():
            if i == value:
                return True
        return False

    def __len__(self):
        return self.length

    def __key_check(self, key):
        if not -self.length <= key < self.length:
            raise IndexError(f'Index {key} out of bounds!')
        return True


@define
class BlockStateLink:
    block_data: BlockStateArray
    index: int

    def get(self) -> int:
        return self.block_data[self.index]

    def set(self, value: int):
        self.block_data[self.index] = value

    def get_palette(self) -> BlockState:
        return self.block_data.palette[self.get()]
