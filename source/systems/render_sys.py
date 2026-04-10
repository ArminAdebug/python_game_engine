from source.components.component import Component
from source.components.sprite import Sprite
from source.components.transform import Transform

from source.object.gameobject import GameObject
from source.directx.directx import DirectX
from source.logging import *

"""
    InputSystem
    ScriptSystem
    AnimationSystem
    PhysicsSystem
    RenderSystem
"""


class RenderSys:

    renderables = {
        Sprite,
    }

    def __init__(self, directx: DirectX):
        self.objects: list[GameObject] = []
        self.directx = directx

    def add(self, game_object: GameObject):
        if not isinstance(game_object, GameObject):
            raise TypeError(
                f"render system expected a game object: <{game_object.__class__.__name__}>")

        if not __class__.renderables & set([type(component) for component in game_object.all_components()]):
            raise ValueError(
                "render system expected at least one renderable component.")

        if self.objects.count(game_object) == 0:
            self.objects.append(game_object)

    def remove(self, game_object: GameObject):
        if not isinstance(game_object, GameObject):
            raise TypeError(
                f"render system expected a game object: <{game_object.__class__.__name__}>")

        if not __class__.renderables & set([type(component) for component in game_object.all_components()]):
            if self.objects.count(game_object) > 0:
                self.objects.remove(game_object)
    def is_registered(self, game_object : GameObject) -> bool:
        return self.objects.count(game_object) > 0

    def render(self):
        """call in render loop
        """
        for game_object in self.objects:

            for component in game_object.all_components():
                match component:
                    case Sprite():
                        self._render_sprite(component, game_object.transform)

    def _render_sprite(self, sprite: Sprite, transform: Transform):
        try:
            self.directx.draw_texture(
                sprite.texture,
                transform.position.x,
                transform.position.y,
                transform.scale.x * sprite.size[0],
                transform.scale.y * sprite.size[1]
            )

        except Exception as e:
            log_exception(repr(e))
