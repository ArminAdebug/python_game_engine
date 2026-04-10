from source.object.gameobject import GameObject
from source.components import Transform
from source.components import Sprite
from source.components import Component
from source.systems.system_registery import Registery
from source.object.gameobject import _game_object_key

class Scene:
    """
    note: dont make scene like this:
    Scene()
    use:
    GameEngine.new_scene(name)
    """


    def __init__(self, name, key, system_registery : Registery):
        self.name = name

        if key != _SceneKey:
            raise RuntimeError("Use GameEngine.new_scene()")

        self.objects: list[GameObject] = []
        self.isActive = True

        self.system_registery = system_registery

    def new_gameobject(self, name):
        obj = GameObject(name, _game_object_key, self)
        self.objects.append(obj)
        return obj


_SceneKey = type("_SceneKey", (), {})
