"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto
from pathlib import Path

import moderngl
from pygame import Vector2


class VSyncMode(Enum):
    """
    Vertical synchronization modes.

    Attributes
    ----------
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

    Attributes
    ----------
    window_size
        Dimensions of the window in pixels.
    target_fps
        FPS target used by the internal clock.
    vsync
        Vertical sync mode.
    """

    window_size: tuple[int, int]
    target_fps: float = 0.0
    vsync: VSyncMode = VSyncMode.CONSTANT


class Comps(StrEnum):
    """ Built-in components expected by the engine. """

    TRANSFORM = auto()
    SPRITE = auto()


@dataclass(slots=True)
class Transform:
    """
    Represents a position, rotation, and scale in 2D space.

    Attributes
    ----------
    position
        2D position in space.
    rotation
        Rotation in degrees.
    scale
        Scale factor. 
    """

    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    scale: float = 1.0


@dataclass(slots=True)
class TextureAsset:
    texture: moderngl.Texture
    name: str
    filepath: Path


@dataclass(slots=True)
class Sprite:
    """
    Represents a renderable 2D image.

    Attributes
    ----------
    texture
        Image of the sprite.
    visible
        Whether this sprite is visible or not.
    tint
        Color tint of the image in range [0, 1].
    alpha
        Opacity of the imaeg in range [0, 1].
    """

    texture: TextureAsset
    visible: bool = True
    tint: float = 0.0
    alpha: float = 1.0