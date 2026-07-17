"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

import sys
import os
from pathlib import Path

from lucid.core.typing import PathLike


def resolve(*children: PathLike) -> Path:
    """ Resolve path in the base directory regardless of freezer. """

    if getattr(sys, "frozen", False):
        base = sys._MEIPASS

    else:
        base = os.getcwd()

    return (Path(base) / Path(*children)).resolve()