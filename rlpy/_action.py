from enum import Enum


class Action(Enum):
    """Class for enumerations of agent actions."""

    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
