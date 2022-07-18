import logging

from attrs import define, field
from nbtlib import Compound, String, Byte

from pymatic.common.container import Container
from pymatic.common.item import Item
from pymatic.common.nbt_object import NBTObject


@define(kw_only=True)
class ItemStack(NBTObject, Container):
    item: Item
    count: int = field(converter=int)
    slot: int = field(converter=int, default=-1)

    _origin: Container = field(default=None)

    @property
    def name(self) -> str:
        return self.item.name

    @property
    def origin(self):
        return self._origin

    @classmethod
    def from_nbt(cls, nbt: Compound | dict) -> 'ItemStack':
        return ItemStack(
            nbt=nbt,
            item=Item[nbt['id']],
            count=nbt['Count'],
            slot=nbt.get('Slot', None)
        )

    def to_nbt(self) -> Compound:
        # self.validate()

        self.nbt.update(Compound({
            'id': String(self.name),
            'Count': Byte(self.count),
            'Slot': Byte(self.slot)
        }))
        if self.slot == -1:
            del self.nbt['Slot']
        return self.nbt

    def validate(self) -> bool:
        res: bool = self._type_validation()

        if self.count > self.item.stack_size:
            logging.warning(f'Unexpected stack size for {self}. Expected {self.item.stack_size}')
            res = False

        return res
