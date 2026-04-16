"""registery components to systems
"""

from source.components import (
    Sprite,
    Script,
    Component
)

from source.logging import Logger


class Registery:
    def __init__(self, systems: dict):
        self.systems = systems

    def update(self, component: Component):
        """update component regesteration on systems

        Args:
            component (Component): component to update
        """

        match component:
            case Sprite():
                try:
                    self.systems["RenderSys"].add(component.game_object)
                except (KeyError, ValueError, TypeError, NameError) as e:
                    Logger.log_exception(
                        "adding component to system failed:", repr(e))
            case Script():
                try:
                    self.systems["ScriptSys"].add(component)
                except (KeyError, ValueError, TypeError, NameError) as e:
                    Logger.log_exception(
                        "adding component to system failed:", repr(e))
