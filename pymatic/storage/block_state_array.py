from abc import ABC, abstractmethod

from attrs import define
from nbtlib.tag import Array

from pymatic.storage.block_state import BlockState
from pymatic.storage.nbt_object import NBTObject


@define(kw_only=True)
class BlockStateArray(NBTObject, ABC):
    block_states: Array
    palette: list[BlockState]
    length: int  # amount of encoded block states

    @abstractmethod
    def block_iterator(self, index: range = None):
        ...

    @abstractmethod
    def get(self, index: int | range) -> int | list:
        ...

    @abstractmethod
    def set(self, index: int | range, value: int):
        ...

    def __setitem__(self, key: int | slice, value: int):
        self.set(key, value)

    def __getitem__(self, key: int | slice) -> int | list:
        if isinstance(key, int):
            return self.get(key)
        if isinstance(key, slice):
            return list(self.block_iterator(index=range(self.length)[key]))
        raise TypeError(f"Invalid key type: {type(key)}")

    def __iter__(self):
        return self.get(range(self.length))
