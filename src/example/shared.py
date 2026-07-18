"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lucid.core import App
    from lucid.asset import AssetManager
    from lucid.input import InputManager

from lucid.models import AppConfig, VSyncMode


# This must exist for the application to initialize.
INITIAL_CONFIG = AppConfig(
    window_size=(1280, 720),
    vsync=VSyncMode.CONSTANT
)

# These services will be automatically assigned by the application instance!
app: "App | None" = None
assets: "AssetManager | None" = None
input: "InputManager | None" = None