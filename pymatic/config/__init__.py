import json
import os.path

import yaml

from attrs import define


@define(frozen=True, kw_only=True)
class _Config:
    mc_version: int
    litematica_version: int
    read_only: bool


with open(os.path.join(__path__[0], '../config/config.yml'), 'r') as f:
    config_file = yaml.load(f, yaml.Loader)

with open(os.path.join(__path__[0], '../config/stack_sizes.json'), 'r') as f:
    STACK_SIZES = json.load(f)

with open(os.path.join(__path__[0], '../config/names.json'), 'r') as f:
    NAMES = json.load(f)

CONFIG = _Config(
    mc_version=config_file['mc_version'],
    litematica_version=config_file['litematica_version'],
    read_only=config_file['read_only']
)
