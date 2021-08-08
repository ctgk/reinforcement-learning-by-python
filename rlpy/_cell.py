from enum import Enum


class Cell(Enum):
    """Class for enumeration of grid cells."""

    NORMAL = 0
    DAMAGE = -1
    REWARD = 1
    BLOCK = 9
