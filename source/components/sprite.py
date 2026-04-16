"""component for rendering Texture"""

from source.components.component import Component
from source.asset.texture import Texture


class Sprite(Component):
    """component for rendering Texture

    Args:
        Component (type): standard Component class

    Raises:
        TypeError: if texture is not instance of Texture.
    """
    type = "sprite"

    def __init__(self, texture: Texture):
        super().__init__()

        if not isinstance(texture, Texture):
            raise TypeError(
                f"Sprite needs an Texture from AssetManager not <{texture.__class__.__name__}>.")

        self.texture = texture
        self.size = texture.size
        self.mode = texture.image_mode

        self.visible = True

    def flip_vertical(self):
        """flip current texture Vertical"""

    def flip_horizenal(self):
        """flip current texture horizenal"""
