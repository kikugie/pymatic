from attrs import define, field
from nbtlib import Compound, LongArray, List

from pymatic.common.block_state import BlockState
from pymatic.common.block_state_array import BlockStateArray


@define(kw_only=True)
class LitematicBlockStateArray(BlockStateArray):
    # block_states: list | Array
    # palette: list[BlockState]
    # length: int  # amount of encoded block states
    _bit_span: int = field(default=None, init=False)  # Amount of bits each entry takes
    _mask: int = field(default=None, init=False)  # 'bit_span' amount of first bits set to 1

    __full_mask = 0b1111111111111111111111111111111111111111111111111111111111111111
    __end_mask = 0b1000000000000000000000000000000000000000000000000000000000000000

    def __attrs_post_init__(self):
        self._bit_span = int.bit_length(len(self.palette) - 1)
        self._mask = (1 << self._bit_span) - 1
        self.block_states = [int(i) & self.__full_mask for i in self.block_states]

    def __array_setup(self, index: int) -> (int, int, int):
        start_offset = index * self._bit_span  # amount of bits to skip
        start_array = start_offset >> 6  # value it reads from
        start_bit_offset = start_offset & 0x3F  # offset in the selected value
        entry_end = start_offset % 64 + self._bit_span  # where palette index will end
        return start_array, start_bit_offset, entry_end

    def get(self, index: int, /) -> int:
        start_array, entry_start, entry_end = self.__array_setup(index)
        # start_array - Long in block states list to read from
        # entry_start - position in the selected Long to start reading from
        # entry_end - position where reading will end

        if entry_end < 64:
            return self.block_states[start_array] >> entry_start & self._mask
            # Shift Long to the point where reading starts, zero all bits after entry end
        else:
            return (self.block_states[start_array] >> entry_start | self.block_states[
                start_array + 1] << 64 - entry_start) & self._mask
            # Combine values from 2 Longs

    def set(self, index: int, value: int, /):
        start_array, entry_start, entry_end = self.__array_setup(index)

        zeroed = self.block_states[start_array] & ~(self._mask << entry_start)
        updated = zeroed | (value & self._mask) << entry_start
        self.block_states[start_array] = updated & self.__full_mask

        if entry_end >= 64:
            self.block_states[start_array] &= self.__full_mask  # Chop off exceeding bits
            shift = 64 - entry_start
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

    def to_nbt(self) -> Compound:
        self.validate()

        self.nbt.update(Compound({
            'BlockStates': LongArray(
                [i | ~self.__full_mask if i & self.__end_mask > 0 else i for i in self.block_states]),
            'BlockStatePalette': List([i.to_nbt() for i in self.palette])
        }))
        return self.nbt

    def validate(self) -> bool:
        return self._type_validation()
