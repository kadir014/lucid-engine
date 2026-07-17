"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from lucid.core import Scene

from example import shared


class Menu(Scene):
    def __init__(self) -> None:
        super().__init__()

    def deactivated(self, next_scene: str) -> None:
        print(f"Menu scene is deactivated. Next is {next_scene}.")

    def activated(self, previous_scene: str) -> None:
        print(f"Menu scene is active! Previous was {previous_scene}.")

    def update(self) -> None:
        shared.app.window_title = f"Example app  -  Menu scene  -  fps: {round(shared.app.fps, 1)}"

        if shared.input.key_pressed("escape"):
            shared.app.stop()

        if shared.input.key_pressed("space"):
            shared.app.scene = "Game"

    def render_before(self) -> None:
        ...