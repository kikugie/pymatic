from attrs import define, field
from nbtlib.tag import Compound, String

from pymatic.common.nbt_object import NBTObject
from pymatic.utils.string_converters import *


@define(kw_only=True)
class BlockState(NBTObject):
    name: str
    properties: dict = field(factory=dict)

    @classmethod
    def from_nbt(cls, nbt: Compound | dict) -> 'BlockState':
        return BlockState(
            nbt=nbt,
            name=str(nbt['Name']),
            properties={k: parse_str(v) for k, v in nbt.get('Properties', {}).items()}
        )

    def to_nbt(self) -> Compound:
        self.validate()

        self.nbt.update(Compound({
            'Name': String(self.name),
            'Properties': Compound({k: String(to_str(v)) for k, v in self.properties.items()})
        }))
        if not self.properties:
            del self.nbt['Properties']
        return self.nbt

    def validate(self) -> bool:
        return self._type_validation()
