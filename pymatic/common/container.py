from pymatic.config import CONFIG


class Container:
    def __init__(self, *, inventory=None):
        if inventory is None:
            self.inventory = []
        self._rec = []
        self._slots = 0

    @property
    def rec_inv(self):
        if CONFIG.read_only:
            return self._rec
        return [i.rec_inv for i in self.inventory].extend(self.inventory)
