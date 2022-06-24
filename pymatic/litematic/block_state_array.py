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
        start_offset = index * self._bit_span  # total amount of bits to skip
        start_array = start_offset >> 6  # array value to read from
        entry_start = start_offset & 0x3F  # offset in the selected value
        entry_end = start_offset % 64 + self._bit_span  # where palette index will end
        return start_array, entry_start, entry_end

    def block_iterator(self, index: range = None):
        if index is None:
            index = range(self.length)
        # Setting up values
        start_offset = index[0] * self._bit_span
        start_array, entry_start, entry_end = self._array_setup(index[0])

        for _ in index:
            if entry_end < 64:
                yield self.block_states[start_array] >> entry_start & self._mask
            else:
                yield (self.block_states[start_array] >> entry_start | self.block_states[
                    start_array + 1] << 64 - entry_start) & self._mask

                start_array += 1
                entry_end -= 64

            # Modifying values only when necessary
            start_offset += self._bit_span
            entry_start = start_offset & 0x3F
            entry_end += self._bit_span

    def get(self, index: int | range) -> int | list:
        if isinstance(index, int):
            index = range(index, index + 1)
        if not (0 <= index[0] < self.length <= index[-1]):
            raise ValueError(f'Index out of bounds: {index}')
        val = self.block_iterator(index)
        return val if len(index) > 1 else next(val)

    def set(self, index: int, value: int):
        start_array, entry_start, entry_end = self._array_setup(index)

        self.block_states[start_array] &= ~(self._mask << entry_start) | (value & self._mask) << entry_start
        # self.block_states[start_array] & ~(self._mask << entry_start) : Zero bits for the value
        # ... | (value & self._mask) << entry_start : Insert value

        if entry_end >= 64:
            self.block_states[start_array] &= 0xFFFFFFFFFFFFFFFF  # Chop off exceeding bits
            shift = 64 - start_array
            self.block_states[start_array + 1] &= ~self._mask >> shift | value >> shift
            # self.block_states[start_array + 1] & ~self._mask >> shift : Zero remaining bits for the value
            # ... | value >> shift : Insert remaining bits


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
