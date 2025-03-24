import collections
from enum import Enum


class Role(Enum):
    EditRole = 0
    DisplayRole = EditRole + 1


EditDisplayRole = collections.namedtuple("EditDisplayRole", ["EditRole", "DisplayRole"])
