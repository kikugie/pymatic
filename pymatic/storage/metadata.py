from abc import ABC, abstractmethod

from pymatic.storage.structure import Structure


class Metadata(ABC):
    @abstractmethod
    def update(self): ...

    @abstractmethod
    def validate(self, structure: Structure): ...
