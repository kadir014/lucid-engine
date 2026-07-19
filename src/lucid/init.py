"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

import os
from importlib.resources import files
from pathlib import Path
import argparse
import re

TEMPLATES = files("lucid.templates")


def mkdir(path: Path) -> None:
    """
    Create directory if not exists.
    
    Parameters
    ----------
    path
        Path to directory
    """

    if os.path.exists(path):
        return
    
    os.mkdir(path)
    print(f"Succesfully created '{path.absolute()}'")


def write(path: Path, content: str, overwrite: bool = False) -> None:
    """
    Create & write to a file.

    Parameters
    ----------
    path
        Path to file
    content
        Content to write
    overwrite
        Overwrite existing file?
    """

    if not overwrite and os.path.exists(path):
        return
    
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
        print(f"Succesfully wrote to '{path.absolute()}'")


def normalize_identifier(name: str) -> str:
    """ Normalize a string into valid Python identifier. """

    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9_]", "_", name)
    if re.match(r"^\d", name):
        name = "_" + name
    return name


def init() -> None:
    """
    Initialize a template Lucid Engine project.
    """

    parser = argparse.ArgumentParser(
        prog="init",
        description="Initialize a Lucid Engine project"
    )

    parser.add_argument(
        "--overwrite",
        help="Overwrite existing files.",
        action="store_true"
    )

    args = parser.parse_args()

    BASE = Path.cwd()
    DESCRIPTION = "Game project with Lucid Engine"
    VERSION = "0.0.1"

    project_name = normalize_identifier(BASE.name)

    project_vars = {
        "project": project_name,
        "desc": DESCRIPTION,
        "version": VERSION
    }

    def read_and_format(fname, project_vars):
        with open(TEMPLATES / fname) as f:
            content = f.read()
        return content.format(**project_vars)

    for fname in ("README.md", "pyproject.toml"):
        doc = read_and_format(TEMPLATES / fname, project_vars)
        write(BASE / fname, doc, args.overwrite)

    mkdir(BASE / "src")
    mkdir(BASE / "src" / project_name)
    mkdir(BASE / "src" / project_name / "scenes")

    doc = read_and_format(TEMPLATES / "__main__.py", project_vars)
    write(BASE / "src" / project_name / "__main__.py", doc, args.overwrite)

    doc = read_and_format(TEMPLATES / "game.py", project_vars)
    write(BASE / "src" / project_name / "scenes" / "game.py", doc, args.overwrite)

    doc = read_and_format(TEMPLATES / "shared.py", project_vars)
    write(BASE / "src" / project_name / "shared.py", doc, args.overwrite)

    cmd = f"$ uv run {project_name}_main"
    print(f"""
··───────··

Your template project using Lucid Engine is all set up!

You can run your app using:
╭─{'─'*len(cmd)}─╮
│ {cmd} │
╰─{'─'*len(cmd)}─╯

Or you can change the entry script name in pyproject.toml file.
Have fun developing! 😊
"""
    )


if __name__ == "__main__":
    init()
