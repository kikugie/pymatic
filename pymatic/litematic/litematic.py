from attrs import define
from nbtlib import Compound

from pymatic.common.region import RegionDict
from pymatic.litematic.litematic_region import LitematicRegion
from pymatic.common.nbt_object import NBTObject
from pymatic.common.structure import Structure


@define
class Litematic(Structure, NBTObject):
    @classmethod
    def from_nbt(cls, nbt: Compound) -> 'Litematic':
        return Litematic(
            nbt=nbt,
            regions=RegionDict({k: LitematicRegion.from_nbt(v) for k, v in nbt['Regions'].items()})
        )

    def to_nbt(self) -> Compound:
        self.nbt.update(Compound({
            k: v.to_nbt() for k, v in self.regions.items()
        }))

        return self.nbt

    def validate(self, *args, **kwargs) -> bool:
        pass
