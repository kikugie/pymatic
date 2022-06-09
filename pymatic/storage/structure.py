import os.path
from abc import ABC

from attrs import define, field
from nbtlib import File

from pymatic.storage.region import Region
from pymatic.storage.nbt_object import NBTObject


@define(kw_only=True)
class Structure(NBTObject, ABC):
    name: str = field(default=None)

    # metadata: MetaData = field(default=None)
    regions: dict[str, Region] = field(factory=dict)

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, 'rb') as f:
            nbt = File.load(f, gzipped=True)
        tmp = cls.from_nbt(nbt)
        tmp.name = os.path.splitext(os.path.basename(file_path))[0]
        return tmp
