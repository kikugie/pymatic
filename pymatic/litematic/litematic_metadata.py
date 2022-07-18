"""
Old and not functional
"""

from time import time

from attrs import define
from nbtlib import String, Int, Long, Compound

from pymatic.config import CONFIG
from pymatic.common.metadata import Metadata
from pymatic.common.nbt_object import NBTObject
from pymatic.common.structure import Structure
from pymatic.utils.vec3d import Vec3d


@define(kw_only=True)
class LitematicMetadata(Metadata, NBTObject):
    author: String = ...
    description: String = String('')
    name: String = ...
    version: Int = Int(CONFIG.litematica_version)
    mc_data_version: Int = Int(CONFIG.mc_data_version)
    region_count: Int = Int(0)
    time_created: Long = Long(time())
    time_modified: Long = Long(time())
    total_blocks: Int = Int(0)
    total_volume: Int = Int(0)
    size: Vec3d[Int, Int, Int] = Vec3d(Int(0), Int(0), Int(0))

    @classmethod
    def from_nbt(cls, nbt: Compound) -> 'LitematicMetadata':
        pass

    def to_nbt(self) -> Compound:
        pass

    def validate(self, structure: Structure):
        pass

    # def validate(self, structure: 'Litematic'):
    #     def validate_fields():
    #         if not super().validate():
    #             logging.error(f'{self.__class__.__name__}: attribute type mismatch')
    #             return False
    #         return True
    #
    #     def validate_region_count():
    #         if self.region_count != len(structure.regions):
    #             logging.error(f'{self.__class__.__name__}: incorrect region count')
    #             return False
    #         return True
    #
    #     def validate_version():
    #         if self.version == 5 and self.mc_data_version in range(1631, 2731):
    #             return True
    #         elif self.version == 6 and self.mc_data_version in range(2825, 2976):
    #             return True
    #         else:
    #             logging.error(f'{self.__class__.__name__}: invalid version')
    #             return False
    #
    #     def validate_time():
    #         if 0 < self.time_created <= self.time_modified:
    #             return True
    #         logging.error(f'{self.__class__.__name__}: invalid time')
    #         return False
    #
    #     def validate_size():
    #         pass
    #
    #     # TODO: make it calculate region positioning and stuff
    #
    #     def validate_blocks():
    #         pass
    #     # TODO: make it count total volume based on size and amount of blocks

    def update(self):
        pass
