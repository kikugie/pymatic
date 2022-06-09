from pprint import pprint

from pymatic.entry_point import NBTFile

lt = NBTFile('schematics/SS2 10 Items Chest Tunnel by KikuGie.litematic')
# print(lt.regions)
# for i in lt.regions['Hall'].block_data:
#     print(lt.regions['Hall'].palette[i])
#
print(lt.regions['Hall'].block_data[0:30:2])


# print(list(lt.regions['Hall'].block_data[0]))
