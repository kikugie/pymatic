import json
import os.path

import yaml

from attrs import define


@define(frozen=True)
class _Config:
    mc_version: int
    litematica_version: int


with open(os.path.join(__path__[0], 'config.yml'), 'r') as f:
    config_file = yaml.load(f, yaml.Loader)

with open(os.path.join(__path__[0], 'stack_sizes.json'), 'r') as f:
    STACK_SIZES = json.load(f)

with open(os.path.join(__path__[0], 'names.json'), 'r') as f:
    NAMES = json.load(f)

CONFIG = _Config(
    mc_version=config_file['mc_version'],
    litematica_version=config_file['litematica_version'],
    i_know_what_i_am_doing=config_file['i_know_what_i_am_doing'],
    read_only=config_file['read_only']
)
