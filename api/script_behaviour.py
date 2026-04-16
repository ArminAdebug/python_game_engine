"""Behaviour class for user code class
"""
from source.components import (
    Script,
    Transform
)

from source.object.gameobject import GameObject


class ScriptBehaviour:
    """Behaviour class for user code class.
    """

    def __init__(self):
        self.this: Script | None = None
        self.game_object: GameObject | None = None
        self.transform: Transform | None = None

    def start(self):
        """runs at game startup
        """

    def update(self):
        """runs on game loop
        """
