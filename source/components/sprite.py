from source.components.component import Component
from typing import *
import os
import numpy as np
from PIL import Image
from source.asset.texture import Texture


class Sprite(Component):
    type = "sprite"

    def __init__(self, texture: Texture):
        super().__init__()

        if not isinstance(texture, Texture):
            raise TypeError(f"Sprite needs an Texture from AssetManager not <{texture.__class__.__name__}>.")

        self.texture = texture
        self.size = texture.size
        self.mode = texture.image_mode

        self.visible = True

    def flip_vertical(self):
        pass

    def flip_horizenal(self):
        pass
