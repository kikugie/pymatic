from attrs import define, field
from nbtlib import Compound, Byte, String

from pymatic.storage.item import Item
from pymatic.storage.nbt_object import NBTObject
from pymatic.storage.container import Container


@define(kw_only=True)
class ItemStack(NBTObject, Container):
    item: Item
    count: Byte
    slot: Byte

    origin: Container = field(default=None)

    @property
    def name(self) -> String:
        return String(self.item.name)

    @classmethod
    def from_nbt(cls, nbt: Compound) -> 'ItemStack':
        tmp = ItemStack(
            nbt=nbt,
            item=Item[nbt['id']],
            count=nbt['Count'],
            slot=nbt.get('Slot', None),
        )
        return tmp

    def to_nbt(self, *args, **kwargs) -> Compound:
        pass

    def validate(self, *args, **kwargs) -> bool:
        pass
