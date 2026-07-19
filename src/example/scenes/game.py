"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from random import randint

import tinyecs as ecs
from pygame import Vector2

from lucid.core import Scene
from lucid.models import Comps, Transform, Sprite

from example import shared


class Game(Scene):
    def __init__(self) -> None:
        super().__init__()

        for _ in range(1000):
            xform = Transform(Vector2(randint(150, 1000), randint(150, 500)))
            sprite = Sprite(shared.assets.texture("tetohead"))

            eid = ecs.create_entity()
            ecs.add_component(eid, Comps.TRANSFORM, xform)
            ecs.add_component(eid, Comps.SPRITE, sprite)
            ecs.add_component(eid, "velocity", Vector2(randint(50, 150)).rotate(randint(0, 360)))

    def deactivated(self, next_scene: str) -> None:
        print(f"Game scene is deactivated. Next is {next_scene}.")

    def activated(self, previous_scene: str) -> None:
        print(f"Game scene is active! Previous was {previous_scene}.")

    def update(self) -> None:
        shared.app.window_title = f"Example app  -  Game scene  -  fps: {round(shared.app.fps, 1)}"

        if shared.input.key_pressed("escape"):
            shared.app.stop()

        if shared.input.key_pressed("space"):
            shared.app.scene = "Menu"

        ecs.run_system(self.move_system, Comps.TRANSFORM, Comps.SPRITE, "velocity")

    def move_system(self, eid: ecs.EntityID, xform: Transform, sprite: Sprite, velocity: Vector2) -> None:
        future_pos = xform.position + velocity * shared.app.dt

        if future_pos.x + 20 > shared.app.window_width or future_pos.x - 20 < 0:
            velocity.x *= -1.0
        
        if future_pos.y + 20 > shared.app.window_height or future_pos.y - 20 < 0:
            velocity.y *= -1.0

        xform.position += velocity * shared.app.dt

        #xform.scale.y = 0.5
        #xform.rotation += 10 * shared.app.dt
        sprite.tint_alpha = xform.position.x / 1280.0