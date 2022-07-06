from attrs import define
from nbtlib import Compound

from pymatic.litematic.litematic_region import LitematicRegion
from pymatic.common.nbt_object import NBTObject
from pymatic.common.structure import Structure


@define
class Litematic(Structure, NBTObject):
    @classmethod
    def from_nbt(cls, nbt: Compound) -> 'Litematic':
        return Litematic(
            nbt=nbt,
            regions={k: LitematicRegion.from_nbt(v) for k, v in nbt['Regions'].items()}
        )

    def to_nbt(self) -> Compound:
        pass

    def validate(self, *args, **kwargs) -> bool:
        pass
