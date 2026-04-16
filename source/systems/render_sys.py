from source.object.gameobject import GameObject
from source.directx.directx import DirectX
from source.logging import Logger
from source.math import Quaternion, Vector3
from source.components import Transform, Sprite


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

        if not any(type(c) in __class__.renderables for c in game_object.all_components()):
            raise ValueError(
                "render system expected at least one renderable component.")

        if self.objects.count(game_object) == 0:
            self.objects.append(game_object)

    def remove(self, game_object: GameObject):
        if not isinstance(game_object, GameObject):
            raise TypeError(
                f"render system expected a game object: <{game_object.__class__.__name__}>")

        if not any(type(c) in __class__.renderables for c in game_object.all_components()):

            if self.objects.count(game_object) > 0:
                self.objects.remove(game_object)

    def is_registered(self, game_object: GameObject) -> bool:
        return self.objects.count(game_object) > 0

    def init_render(self):
        pass

    def render(self):
        """call in render loop
        """
        for game_object in self.objects:

            for component in game_object.all_components():
                match component:
                    case Sprite():
                        self._render_sprite(component, game_object.transform)

    def _render_sprite(self, sprite: Sprite, transform: Transform):
        """render sprite on screen with game object transform

        Args:
            sprite (Sprite): sprite component
            transform (Transform): game object transform
        """

        if not sprite.visible:
            return

        quat: Quaternion = transform.rotation
        p1 = (
            (-sprite.size[0] * transform.scale.x/2, -
             sprite.size[1] * transform.scale.y/2, 0),
            (+sprite.size[0] * transform.scale.x/2, -
             sprite.size[1] * transform.scale.y/2, 0),
            (-sprite.size[0] * transform.scale.x/2, +
             sprite.size[1] * transform.scale.y/2, 0),
            (+sprite.size[0] * transform.scale.x/2, +
             sprite.size[1] * transform.scale.y/2, 0)
        )

        p2 = []

        for x, y, z in p1:

            p = Quaternion(
                x,
                y,
                z,
                0
            )

            q_conjugate = Quaternion(
                quat.x * -1,
                quat.y * -1,
                quat.z * -1,
                quat.w
            )

            point = quat * p * q_conjugate
            p2.append(Vector3(point.x, point.y, point.z))

        try:
            self.directx.draw_texture(
                sprite.texture.texture,
                p2[0] + transform.position,
                p2[1] + transform.position,
                p2[2] + transform.position,
                p2[3] + transform.position,
            )

        except Exception as e:
            Logger.log_exception(repr(e))
