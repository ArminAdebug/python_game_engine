from source.components import *
from source.logging import *


class Registery:
    def __init__(self, systems: dict):
        self.systems = systems

    def update(self, component: Component):
        match component:
            case Sprite():
                try:
                    self.systems["RenderSys"].add(component.game_object)
                except Exception as e:
                    log_exception(
                        "adding component to system failed:", repr(e))
            case Script():
                try:
                    self.systems["ScriptSys"].add(component)
                except Exception as e:
                    log_exception(
                        "adding component to system failed:", repr(e))
