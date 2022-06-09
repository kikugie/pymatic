import re
from typing import ClassVar

from attrs import define, field
from nbtlib import String

from pymatic.config import STACK_SIZES, NAMES


@define
class Item:
    id: str
    stack_size: int
    name: str = field(default=None)
    _all: ClassVar[dict] = {}

    @staticmethod
    def _generate_item(name: str | String) -> 'Item':
        name = str(name)
        tmp = Item(
            id=name,
            stack_size=STACK_SIZES.get(name, 64),
            name=NAMES.get(name, None),
        )
        Item._all[name] = tmp
        return tmp

    @classmethod
    def get(cls, name: str | String, default=None) -> 'Item':
        name = str(name)
        if name in cls._all:
            return cls._all[name]
        if default is not None:
            return default
        if not re.fullmatch(r'\w+:\w+', name):
            raise ValueError(f'Invalid item name: {name}')
        return cls._generate_item(name)

    def __class_getitem__(cls, item):
        return cls.get(item)

    @property
    def all_items(self) -> dict:
        return self._all
