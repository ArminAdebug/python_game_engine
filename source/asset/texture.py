from dataclasses import dataclass
from pathlib import Path
from typing import *


@dataclass
class Texture:
    texture: int
    size: tuple[int, int]
    path: Path | str = ""
    image_mode: str = ""


if __name__ == "__main__":
    t = Texture(5, (500, 500), "c:\\", "RGB")
    print(t)
