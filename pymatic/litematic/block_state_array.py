from attrs import define
from nbtlib import Compound

from pymatic.errors import BlockOutOfBounds
from pymatic.storage.block_state import BlockState
from pymatic.storage.block_state_array import BlockStateArray


@define(kw_only=True)
class LitematicBlockStateArray(BlockStateArray):
    _bit_span: int = None
    _mask: int = None

    def __attrs_post_init__(self):
        self._bit_span = int.bit_length(len(self.palette) - 1)
        self._mask = (1 << self._bit_span) - 1

    def _array_setup(self, index: int) -> (int, int, int):
        start_offset = index * self._bit_span  # amount of bits to skip
        start_array = start_offset >> 6  # value it reads from
        start_bit_offset = start_offset & 0x3F  # offset in the selected value
        entry_end = start_offset % 64 + self._bit_span  # where palette index will end
        return start_array, start_bit_offset, entry_end

    def block_iterator(self, index: range = None):
        if index is None:
            index = range(self.length)
        # elif index[0] < 0 or index[-1] >= self.length:
        #     raise BlockOutOfBounds(f'Attempted to access out of bounds block at {index}')
        # Setting up values
        start_offset = index[0] * self._bit_span
        start_array, start_bit_offset, entry_end = self._array_setup(index[0])

        for i in index:
            if entry_end < 64:
                out = self.block_states[start_array] >> start_bit_offset & self._mask
            else:
                end_offset = 64 - start_bit_offset
                end_array = ((i + 1) * self._bit_span - 1) >> 6
                out = (abs(self.block_states[start_array] >> start_bit_offset) | self.block_states[
                    end_array] << end_offset) & self._mask

                start_array += 1
                entry_end -= 64

            # Modifying values only when necessary
            start_offset += self._bit_span
            start_bit_offset = start_offset & 0x3F
            entry_end += self._bit_span

            yield out

    def get(self, index: int | range) -> int | list:
        if isinstance(index, int):
            index = range(index, index + 1)
        val = self.block_iterator(index)
        return val if len(index) > 1 else next(val)

    def set(self, index: int, value: int):
        start_array, start_bit_offset, entry_end = self._array_setup(index)

    @classmethod
    def from_nbt(cls, nbt: Compound) -> 'LitematicBlockStateArray':
        return LitematicBlockStateArray(
            palette=[BlockState.from_nbt(i) for i in nbt['BlockStatePalette']],
            block_states=nbt['BlockStates'],
            length=abs(nbt['Size']['x'] * nbt['Size']['y'] * nbt['Size']['z'])
        )

    def to_nbt(self, *args, **kwargs) -> Compound:
        pass

    def validate(self, *args, **kwargs) -> bool:
        pass
