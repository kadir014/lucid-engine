"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

from pathlib import Path

import moderngl
import pygame

from lucid.core.typing import PathLike
from lucid.core.log import debug
from lucid.core.path import resolve
from lucid.models import TextureAsset


class AssetManager:
    def __init__(self, context: moderngl.Context) -> None:
        self._context = context

        self._font_paths: dict[str, Path] = {}
        self._texture_paths: dict[str, Path] = {}

        self._fonts: dict[str, pygame.Font] = {}
        self._textures: dict[str, TextureAsset] = {}

        self._fallback_font = pygame.Font(None)

    def _load_textures(self) -> None:
        for name, path in self._texture_paths.items():
            surf = pygame.image.load(path)
            format = "RGB" if surf.get_bytesize() == 3 else "RGBA"
            tex = self._context.texture(
                surf.get_size(),
                len(format),
                pygame.image.tobytes(surf, format, False)
            )
            self._textures[name] = TextureAsset(tex, name, path)

            debug(f"Texture <fg.yellow>{name}</> loaded at <fg.darkgray>{str(path)}</>")

    def load(self, assets_path: PathLike) -> None:
        assets = resolve(assets_path)

        for root, _, files in assets.walk():
            if root.stem == "textures":
                for file in files:
                    final_path = root / file
                    self._texture_paths[final_path.stem] = final_path

            elif root.stem == "fonts":
                for file in files:
                    final_path = root / file
                    self._font_paths[final_path.stem] = final_path

        self._load_textures()

    def font(self, name: str, size: int = 24) -> pygame.Font:
        # Cached
        if (name, size) in self._fonts:
            return self._fonts[(name, size)]

        # Not cached
        elif name in self._font_paths:
            font = pygame.Font(self._font_paths[name], size)
            self._fonts[(name, size)] = font
            return font

        # Not even found in assets directory, return the fallback font
        else:
            return self._fallback_font
        
    def texture(self, name: str) -> TextureAsset:
        return self._textures[name]