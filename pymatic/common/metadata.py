"""
W.I.P. Metadata editing
"""

from abc import ABC, abstractmethod

from pymatic.common.structure import Structure


class Metadata(ABC):
    @abstractmethod
    def update(self): ...

    @abstractmethod
    def validate(self, structure: Structure): ...
