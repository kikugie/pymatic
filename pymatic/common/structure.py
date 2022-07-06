import os.path
from abc import ABC

from attrs import define, field
from nbtlib import load, File

from pymatic.common.region import Region
from pymatic.common.nbt_object import NBTObject


@define(kw_only=True)
class Structure(NBTObject, ABC):
    name: str = field(default=None)
    filetype: str = field(default=None)

    # metadata: MetaData = field(default=None)
    regions: dict[str, Region] = field(factory=dict)

    @classmethod
    def from_file(cls, file_path: str, gzipped: bool = None):
        nbt = load(file_path, gzipped=gzipped)
        tmp = cls.from_nbt(nbt)
        file = os.path.splitext(os.path.basename(file_path))
        tmp.name = file[0]
        tmp.filetype = file[1]
        return tmp

    def to_file(self, filename: str = None, gzipped: bool = None):
        File(self.nbt).save(filename, gzipped=gzipped)
