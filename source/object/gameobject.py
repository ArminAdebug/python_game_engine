from __future__ import annotations
from typing import TYPE_CHECKING

from source.components import (
    Component,
    Transform,
)


if TYPE_CHECKING:
    from source.object.scene import Scene


class GameObject:
    """
    note: dont make object like this:
    GameObject()
    use:
    scene.new_gameobject(name)
    """

    def __init__(self, name, key, scene: Scene):
        from source.object.scene import Scene

        if not isinstance(scene, Scene):
            raise TypeError(
                "game Object needs to create from Scene.new_gameobject")

        if key != _game_object_key:
            raise RuntimeError("Use scene.new_gameobject()")

        self.scene = scene

        self.name = name
        self.components: list[Component] = []

        self.transform = Transform()
        self.components.append(self.transform)

    def add_component(self, component: Component):
        if not isinstance(component, Component):
            raise TypeError("add_component expect a Component.")

        if isinstance(component, Transform):
            raise TypeError(
                "GameObject only can have one Transform component.")

        component.game_object = self
        self.components.append(component)
        self.scene.system_registery.update(component)

    def get_component(self, component_type: Component) -> list[Component]:

        founds = []

        for com in self.components:
            if type(com) == component_type:
                founds.append(com)

        return founds

    def remove_component(self, component_target: Component) -> list[Component]:
        """remove all component with a target type

        Args:
            component_target (Component): component target type
        """
        for component in self.components:
            if type(component) == type(component_target):
                self.components.remove(component)

        self.scene.system_registery.update(component_target)

    def all_components(self) -> list[Component]:
        """
        return a list of game object components

        Returns:
            list[Component]: all game object components
        """

        return self.components

    def __str__(self):
        return f"""{self.name}:\n{self.components}"""


# key for making GameObject
_game_object_key = type("_GameObjectKey", (), {}
                        )  # pylint: disable=C0103, too-few-public-methods
