from abc import ABC

from attrs import define, field

from pymatic.common.nbt_object import NBTObject
from pymatic.common.block_state_array import BlockStateArray
from pymatic.utils.vec3d import Vec3d


@define(kw_only=True)
class Region(NBTObject, ABC):
    block_data: BlockStateArray = field(default=None)
    # tile_entities: list[TileEntity] = field(default=None)
    # entities: list[Entity] = field(default=None)

    size: Vec3d = field(default=None)

    @property
    def block_states(self):
        return self.block_data.block_states

    @property
    def palette(self):
        return self.block_data.palette

    @property
    def volume(self):
        return abs(self.size.x * self.size.y * self.size.z)
