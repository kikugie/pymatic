from nbtlib import Compound

from pymatic.litematic.block_state_array import LitematicBlockStateArray
from pymatic.storage.nbt_object import NBTObject
from pymatic.storage.region import Region
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
        pass

    def validate(self, *args, **kwargs) -> bool:
        pass
