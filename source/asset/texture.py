"""have texture class for texture data
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Texture:
    """dataclass of Texture for Textures data
    """
    texture: int
    size: tuple[int, int]
    path: Path | str = ""
    image_mode: str = ""

# testing texture
if __name__ == "__main__":
    t = Texture(5, (500, 500), "c:\\", "RGB")
    print(t)
