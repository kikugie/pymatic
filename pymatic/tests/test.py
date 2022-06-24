from pymatic.entry_point import NBTFile

lt = NBTFile('schematics/SS2 10 Items Chest Tunnel by KikuGie.litematic')
lt.regions['Hall'].block_data.block_states[0] = 0
# for i in range(lt.regions['Hall'].volume):
#     lt.regions['Hall'].block_data.set(i, 5)
print('done')