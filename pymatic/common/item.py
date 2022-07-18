import re

from pymatic.config import STACK_SIZES, NAMES


class Item:
    _all: dict = {}

    def __init__(self, item_id: str):
        self.id: str = item_id
        self.stack_size: int = STACK_SIZES.get(item_id, 64)
        self.name: str = NAMES.get(item_id, None)

        self.__class__._all[item_id] = self

    @classmethod
    def get(cls, name: str) -> 'Item':
        name = str(name)
        if name in cls._all:
            return cls._all[name]
        if not re.fullmatch(r'\w+:\w+', name):
            raise ValueError(f'Invalid item name: {name}')
        return Item(name)

    def __class_getitem__(cls, item):
        return cls.get(item)

    @property
    def all_items(self) -> dict:
        return self._all
