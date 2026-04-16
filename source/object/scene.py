from source.object.gameobject import GameObject
from source.systems.system_registery import Registery
from source.object.gameobject import _game_object_key


class Scene:
    """
    note: dont make scene like this:
    Scene()
    use:
    GameEngine.new_scene(name)
    """

    def __init__(self, name: str, key: "_SceneKey", system_registery: Registery):
        self.name = name

        if key != _SceneKey:
            raise RuntimeError("Use GameEngine.new_scene()")

        self.objects: list[GameObject] = []
        self.is_active = True

        self.system_registery: Registery = system_registery

    def new_gameobject(self, name: str) -> GameObject:
        """create new Game object in scene

        Args:
            name (str): name of new Game Object

        Returns:
            GameObject: new GameObject
        """

        obj = GameObject(name, _game_object_key, self)
        self.objects.append(obj)
        return obj


_SceneKey = type("_SceneKey", (), {})  # pylint: disable=C0103, too-few-public-methods
