from abc import ABC, abstractmethod
from attrs import define, field, fields
from nbtlib import Compound


@define(kw_only=True, slots=True)
class NBTObject(ABC):
    """
    Base class for NBT objects.
    """
    nbt: Compound = field(factory=Compound)

    @classmethod
    @abstractmethod
    def from_nbt(cls, nbt: Compound) -> 'NBTObject':
        """
        Parses nbtlib Compound into an object.
        """
        ...

    @abstractmethod
    def to_nbt(self, *args, **kwargs) -> Compound:
        """
        Validates and converts object into nbtlib Compound.
        """
        ...

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        """
        Validates the object.
        """
        ...

    def _type_validation(self) -> bool:
        for att in fields(self.__class__):
            if not isinstance(getattr(self, att.name), att.type):
                return False
        return True
