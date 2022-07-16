from attrs import define, field
from nbtlib import Compound

from pymatic.common.container import Container
from pymatic.common.item_stack import ItemStack
from pymatic.common.nbt_object import NBTObject
from pymatic.utils.vec3d import Vec3d


@define(kw_only=True)
class TileEntity(NBTObject):
    pos: Vec3d
    id: str = field(default=None)

    @classmethod
    def from_nbt(cls, nbt: Compound | dict) -> 'TileEntity':
        if 'Items' in nbt:
            return ContainerTileEntity.from_nbt(nbt)
        return TileEntity(
            nbt=nbt,
            pos=Vec3d(int(nbt['x']), int(nbt['y']), int(nbt['z']))
        )

    def to_nbt(self) -> Compound:
        pass

    def validate(self) -> bool:
        pass


@define(kw_only=True)
class ContainerTileEntity(TileEntity, Container):
    inventory: list = field(factory=list)

    @classmethod
    def from_nbt(cls, nbt: Compound | dict) -> 'ContainerTileEntity':
        return ContainerTileEntity(
            nbt=nbt,
            pos=Vec3d(int(nbt['x']), int(nbt['y']), int(nbt['z'])),
            inventory=[ItemStack.from_nbt(i) for i in nbt['Items']]
        )


a = {'Items': [], 'x': 0, 'y': 0, 'z': 0}
b = TileEntity.from_nbt(a)
