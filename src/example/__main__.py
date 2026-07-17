"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from lucid.core import App

from example import shared
from example.scenes.menu import Menu
from example.scenes.game import Game


def main() -> None:
    app = App(shared)

    app.add_scene(Menu)
    app.add_scene(Game)

    app.scene = "Menu"

    app.run()


if __name__ == "__main__":
    main()