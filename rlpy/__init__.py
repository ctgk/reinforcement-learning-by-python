"""Unofficial package of Reinforcement Learning by Python."""

from rlpy._state import State

__version__ = '0.0.1'


_classes = [
    State,
]


for _cls in _classes:
    _cls.__module__ = __name__


__all__ = [_cls.__name__ for _cls in _classes]


del _cls
del _classes
