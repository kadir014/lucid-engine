"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from typing import Protocol

from pathlib import Path

from lucid.models import AppConfig


class SharedModule(Protocol):
    INITIAL_CONFIG: AppConfig


PathLike = Path | str | bytes