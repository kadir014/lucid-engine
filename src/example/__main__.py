"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

import sys

from lucid.core import App, log

from example import shared
from example.scenes.menu import Menu
from example.scenes.game import Game


def main() -> None:
    log.targets.add(
        log.LogTarget(sys.stdout, colored=True, min_level=log.LogLevel.DEBUG)
    )

    app = App(shared)
    # People are going to run example demo from the root directory, hence this path
    shared.assets.load("src/example/assets")

    app.add_scene(Menu)
    app.add_scene(Game)

    app.scene = "Menu"

    app.run()


if __name__ == "__main__":
    main()