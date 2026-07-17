"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from dataclasses import dataclass, field
from enum import Enum

from pygame import Vector2


class VSyncMode(Enum):
    """
    Vertical synchronization modes.

    Fields
    ------
    NONE
        No vertical sync.
    CONSTANT
        Regular vsync, display is synced with monitor's refresh rate.
    ADAPTIVE
        OpenGL's adaptive sync mode.
    """

    NONE = 0
    CONSTANT = 1
    ADAPTIVE = -1


@dataclass
class AppConfig:
    """
    Initial application configuration record.
    """

    window_size: tuple[int, int]
    target_fps: float = 0.0
    vsync: VSyncMode = VSyncMode.CONSTANT


@dataclass
class Transform:
    """
    Represents a position, rotation, and scale in 2D space.
    """

    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    scale: float = 1.0