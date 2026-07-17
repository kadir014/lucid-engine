"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from typing import TYPE_CHECKING

import pygame

from lucid.models import Transform
    

class Scene:
    """
    Represents an active game world.

    A scene owns the entities, systems, and global state required to
    simulate and render a portion of the game.

    Attributes
    ----------
    camera
        Camera transform used when rendering the scene.
    """

    def __init__(self) -> None:
        self.camera = Transform()

    def activated(self, previous_scene: str) -> None:
        """
        Callback called whenever this scene is activated.
        
        You can implement this method in your subclass.

        Parameters
        ----------
        previous_scene
            Name of the previous scene, empty if none.
        """
        ...

    def deactivated(self, next_scene: str) -> None:
        """
        Callback called whenever this scene is deactivated.
        
        You can implement this method in your subclass.

        Parameters
        ----------
        next_scene
            Name of the next scene, empty if none.
        """
        ...

    def update(self) -> None:
        """
        Scene update callback, this is called before updating all entities.
        
        You can implement this method in your subclass.
        """
        ...

    def render_before(self) -> None:
        """
        Scene render callback before drawing entities.
        
        You can implement this method in your subclass.
        """
        ...

    def render_after(self) -> None:
        """
        Scene render callback after drawing entities.
        
        You can implement this method in your subclass.
        """
        ...