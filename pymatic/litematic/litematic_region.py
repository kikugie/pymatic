from nbtlib import Compound

from pymatic.litematic.litematic_block_state_array import LitematicBlockStateArray
from pymatic.common.nbt_object import NBTObject
from pymatic.common.region import Region
from pymatic.utils.vec3d import Vec3d


class LitematicRegion(Region, NBTObject):
    @classmethod
    def from_nbt(cls, nbt: Compound) -> 'LitematicRegion':
        tmp = LitematicRegion()
        tmp.nbt = nbt
        tmp.size = Vec3d(**nbt['Size'])

        tmp.block_data = LitematicBlockStateArray.from_nbt(nbt)
        return tmp

    def to_nbt(self, *args, **kwargs) -> Compound:
        self.nbt.update(self.block_data.to_nbt())
        # TODO: write other values
        return self.nbt

    def validate(self, *args, **kwargs) -> bool:
        pass
