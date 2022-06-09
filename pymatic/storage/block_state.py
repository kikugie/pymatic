import logging

from attrs import define
from nbtlib.tag import Compound, String

from pymatic.storage.nbt_object import NBTObject
from pymatic.utils.string_converters import conv_str, to_str


@define(kw_only=True)
class BlockState(NBTObject):
    name: String
    properties: Compound

    @classmethod
    def from_nbt(cls, nbt: Compound) -> 'BlockState':
        return BlockState(
            nbt=nbt,
            name=nbt['Name'],
            properties={k: conv_str(v) for k, v in nbt.get('Properties', {}).items()}
        )

    def to_nbt(self, *args, **kwargs) -> Compound:
        if not self.validate():
            logging.error(f'Failed to write block state: {self}')
            raise ValueError('Invalid BlockState')

        out = Compound()
        out['Name'] = self.name
        if self.properties:
            out['Properties'] = Compound({k: to_str(v) for k, v in self.properties.items()})
        return out

    def validate(self, *args, **kwargs) -> bool:
        return self._type_validation()
