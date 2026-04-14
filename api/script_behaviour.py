from source.components import (
    Component,
    Script,
    Transform
)

from source.object.gameobject import GameObject
from typing import *


class ScriptBehaviour:
    def __init__(self):
        self.this: Script | None = None
        self.game_object: GameObject | None = None
        self.transform: Transform | None = None

    def start():
        pass

    def update():
        pass
