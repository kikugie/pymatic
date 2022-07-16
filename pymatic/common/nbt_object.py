import logging
from abc import ABC, abstractmethod

from attrs import define, field, fields
from nbtlib import Compound

from pymatic.config import CONFIG


@define(kw_only=True, slots=True)
class NBTObject(ABC):
    """
    General abstract class for classes that represent nbt data.
    """
    nbt: Compound = field(factory=Compound)

    @classmethod
    @abstractmethod
    def from_nbt(cls, nbt: Compound | dict) -> 'NBTObject':
        """
        Parses nbtlib Compound into an object.
        """
        ...

    @abstractmethod
    def to_nbt(self) -> Compound:
        """
        Validates and converts object into nbtlib Compound.
        """
        ...

    @abstractmethod
    def validate(self) -> bool:
        """
        Validates the object.
        """
        ...

    def _type_validation(self) -> bool:
        # noinspection PyDataclass
        for att in fields(self.__class__):
            if not (att.name.startswith('_') or isinstance(t := getattr(self, att.name), att.type)):
                logging.error(f"Incorrect attribute type for '{att.name}' at {self}.")
                raise TypeError(f"Unexpected type {type(t)} for attribute '{att.name}'. Expected {att.type}.")
        return True

    def _write_validation(self):
        if CONFIG.read_only:
            raise Exception(f'Unable to write')
