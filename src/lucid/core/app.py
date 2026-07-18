"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from os import environ
import asyncio
from time import time

import pygame
import miniprofiler
import tinyecs as ecs

from lucid.core.typing import SharedModule, PathLike
from lucid.core.path import resolve
from lucid.core.scene import Scene
from lucid.models import VSyncMode, Comps, Transform, Sprite
from lucid.asset import AssetManager
from lucid.input import InputManager
from lucid.rendering import Renderer


class App:
    """
    Top-level application class.

    Attributes
    ----------
    target_fps
        Targeted FPS cap
    dt_cap
        Maximum deltatime in seconds
    scenes
        A dictionary of scene names and scene instances
    """

    def __init__(self, sharedmod: SharedModule) -> None:
        """
        Parameters
        ----------
        sharedmod
            Shared module with initialized initial configuration.
        """

        config = sharedmod.INITIAL_CONFIG

        # Fix desktop scaling on wayland, thanks to DD
        if environ.get("XDG_SESSION_TYPE", "") == "wayland":
            environ["SDL_VIDEODRIVER"] = "wayland"

        pygame.init()

        self._clock = pygame.time.Clock()
        
        self.target_fps = config.target_fps
        self.dt_cap = 0.25

        self._events: list[pygame.Event] = []
        self._fps = self.target_fps
        self._dt = 0.0
        self._is_running = False
        self._start_time = 0.0
        self._time = 0.0

        self._window_title = ""

        self._vsync = config.vsync
        self._window_width, self._window_height = config.window_size
        self.create_window()

        self.scenes: dict[str, Scene] = {}
        self._current_scene = ""

        self.profiler = miniprofiler.Profiler(60)

        self.renderer = Renderer()
        self._assets = sharedmod.assets = AssetManager(self.renderer.context)
        self._input = sharedmod.input = InputManager()
        sharedmod.app = self

    @property
    def events(self) -> list[pygame.Event]:
        """ Events polled in the current frame. """
        return self._events
    
    @property
    def fps(self) -> float:
        """ Current FPS. """
        return self._fps
    
    @property
    def dt(self) -> float:
        """ Current deltatime in seconds. """
        return self._dt
    
    @property
    def is_running(self) -> bool:
        """ Is the app currently running? """
        return self._is_running
    
    @property
    def time(self) -> float:
        """ Elapsed time since app started running in seconds. """
        return self._time

    @property
    def window_width(self) -> int:
        """ Width of window in pixels. """
        return self._window_width
    
    @window_width.setter
    def window_width(self, value: int) -> None:
        self._window_width = value
        self.create_window()

    @property
    def window_height(self) -> int:
        """ Height of window in pixels. """
        return self._window_height
    
    @window_height.setter
    def window_height(self, value: int) -> None:
        self._window_height = value
        self.create_window()

    @property
    def vsync(self) -> VSyncMode:
        """ VSync mode of the window. """
        return self._vsync
    
    @vsync.setter
    def vsync(self, value: VSyncMode) -> None:
        self._vsync = value
        self.create_window()

    @property
    def global_window_frect(self) -> pygame.FRect:
        """ Global window geometry as an FRect. """
        pos = pygame.display.get_window_position()
        return pygame.FRect(
            pos[0], pos[1], self._window_width, self._window_height
        )
    
    @property
    def global_window_rect(self) -> pygame.Rect:
        """ Global window geometry as a Rect. """
        rect = self.window_frect
        return pygame.Rect(rect.x, rect.y, rect.w, rect.h)
    
    @property
    def window_frect(self) -> pygame.FRect:
        """ Local window geometry as an FRect. """
        return pygame.FRect(
            0.0, 0.0, self._window_width, self._window_height
        )
    
    @property
    def window_rect(self) -> pygame.Rect:
        """ Local window geometry as a Rect. """
        return pygame.Rect(
            0.0, 0.0, self._window_width, self._window_height
        )
    
    @property
    def aspect_ratio(self) -> float:
        """ Current aspect ratio of the resolution (width over height). """
        return self._window_width / self._window_height

    @property
    def window_title(self) -> str:
        """ Text string of the window title. """
        return self._window_title
    
    @window_title.setter
    def window_title(self, value: str) -> None:
        self._window_title = value
        pygame.display.set_caption(self._window_title)

    def create_window(self) -> None:
        """ Create window with the current resolution. """
        
        self.display = pygame.display.set_mode(
            (self._window_width, self._window_height),
            vsync=self._vsync.value,
            flags=pygame.OPENGL | pygame.DOUBLEBUF
        )

    def set_window_icon(self, filepath: PathLike) -> None:
        """
        Load & set window icon.
        
        Parameters
        ----------
        filepath
            Path to the window icon.
        """
        # TODO: This must be asset manager's responsibility
        pygame.display.set_icon(pygame.image.load(resolve(filepath)))

    def add_scene(self, scene: Scene) -> None:
        """
        Add a scene to the application.

        Scene classes are initialized upon adding them to the application.

        Parameters
        ----------
        scene
            Scene class to add.
        """
        scene_ = scene()
        self.scenes[scene_.__class__.__name__] = scene_

    @property
    def scene(self) -> Scene:
        """ Current active scene. """
        return self.scenes[self._current_scene]
    
    @scene.setter
    def scene(self, scene_name: str) -> None:
        previous = self._current_scene
        if previous:
            self.scenes[previous].deactivated(scene_name)
        
        self._current_scene = scene_name
        self.scenes[self._current_scene].activated(previous)

    def stop(self) -> None:
        """ Stop the application. """
        self._is_running = False

    def run(self) -> None:
        """ Run the application. """

        self._is_running = True
        self._start_time = time()

        while self._is_running:
            self.tick()
        
        pygame.quit()

    async def run_async(self) -> None:
        """ Run the application asynchronously for web. """

        self._is_running = True
        self._start_time = time()

        while self._is_running:
            self.tick()

            await asyncio.sleep(0)

        pygame.quit()

    def tick(self) -> None:
        """ One game frame. """

        with self.profiler.profile("frame"):

            self._dt = self._clock.tick(self.target_fps) * 0.001
            self._dt = min(self._dt, self.dt_cap)

            self._fps = self._clock.get_fps()
            # Prevent OverflowError for rendering
            if self._fps == float("inf") or self._fps == -float("inf"):
                self._fps = 0

            self._time = time() - self._start_time

            with self.profiler.profile("update"):
                self._update()

            with self.profiler.profile("render"):
                self._render()

    def _update(self) -> None:
        """ Update the game frame. """

        self._events = pygame.event.get()

        for event in self._events:
            if event.type == pygame.QUIT:
                self.stop()

        self._input.update(self.events)

        self.scene.update()

    def _render(self) -> None:
        """ Render the game frame. """

        ecs.run_system(self._render_system, Comps.TRANSFORM, Comps.SPRITE)

        self.renderer.render((self._window_width, self._window_height))

        pygame.display.flip()

    def _render_system(self, eid: ecs.EntityID, xform: Transform, sprite: Sprite) -> None:
        if not sprite.visible:
            return
        
        self.renderer.batch_sprite(
            xform, sprite, sprite.texture.name
        )