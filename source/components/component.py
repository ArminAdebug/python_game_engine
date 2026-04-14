from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.object.gameobject import GameObject


class Component:
    type = None

    def __init__(self):
        self.game_object: None | GameObject = None
