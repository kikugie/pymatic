from attrs import define, field

from pymatic.config import CONFIG


@define
class Container:
    inventory: list = field(factory=list)
    _rec: list = field(factory=list)  # Recursive inventory. List of all nested items
    _slots: int = field(default=0)  # TODO remove if not used

    @property
    def rec_inv(self):
        if CONFIG.read_only:
            return self._rec
        return [i.rec_inv for i in self.inventory].extend(self.inventory)
