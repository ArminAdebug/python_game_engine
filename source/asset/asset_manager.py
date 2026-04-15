from pathlib import Path

from typing import TYPE_CHECKING
from source.components import Component
from typing import *
import os
import numpy as np
from PIL import Image
from source.asset.texture import Texture

if TYPE_CHECKING:
    from source.directx.directx import DirectX


class AssetManager:
    def __init__(self, directx : "DirectX"):
        self.directx = directx

    def load_image(self, file_path: Path | str) -> tuple[int, tuple[int, int]]:
        """

        Args:
            file_path (Path | str): image path

        Raises:
            FileNotFoundError

        Returns:
            tuple[int, tuple[int, int]]: texture pointer for directx and image size
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file {file_path} doesn's exists.")

        image = Image.open(file_path)
        image_format = image.format
        image = image.convert("RGBA")
        size = image.size

        bgra_array = self._convert2argb(image)

        texture: int = self.directx.create_texture_from_argb(
            bgra_array
        )
        return Texture(texture, size, path=file_path, image_mode=image_format)

    def _convert2argb(self, image):
        rgba = np.array(image, dtype=np.uint8)
        # bgra = rgba[:, :, [0,3,2,1]]  # swap R and B
        r = rgba[::, ::, 0]
        g = rgba[::, ::, 1]
        b = rgba[::, ::, 2]
        a = rgba[::, ::, 3]

        bgra = np.stack((b, g, r, a), axis=-1)
        return bgra
