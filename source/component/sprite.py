from source.component.component import Component
from typing import *
import os
import numpy as np
from PIL import Image


class Sprite(Component):
    def __init__(self, image_file_path, directx):
        if not os.path.exists(image_file_path):
            raise FileNotFoundError(f"file {image_file_path} doesn's exists.")

        self.image = Image.open(image_file_path).convert("RGBA")
        self.size = self.image.size

        self.pixel_array = self._convert2argb()

        self.texture = directx.create_texture_from_argb(
            self.pixel_array
        )

    def _convert2argb(self):

        rgba = np.array(self.image, dtype=np.uint32)

        r = rgba[:, :, 0]
        g = rgba[:, :, 1]
        b = rgba[:, :, 2]
        a = rgba[:, :, 3]

        argb = np.stack([a, r, g, b], axis=-1)

        return argb
