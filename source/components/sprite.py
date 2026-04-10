from source.components.component import Component
from typing import *
import os
import numpy as np
from PIL import Image


class Sprite(Component):
    type = "sprite"

    def __init__(self, image_file_path, directx):
        super().__init__()
        if not os.path.exists(image_file_path):
            raise FileNotFoundError(f"file {image_file_path} doesn's exists.")

        self.image = Image.open(image_file_path).convert("RGBA")
        self.size = self.image.size

        self.bgra_array = self._convert2argb()

        self.texture = directx.create_texture_from_argb(
            self.bgra_array
        )

    def _convert2argb(self):
        rgba = np.array(self.image, dtype=np.uint8)
        # bgra = rgba[:, :, [0,3,2,1]]  # swap R and B
        r = rgba[::, ::, 0]
        g = rgba[::, ::, 1]
        b = rgba[::, ::, 2]
        a = rgba[::, ::, 3]

        bgra = np.stack((b, g, r, a), axis=-1)
        return bgra
