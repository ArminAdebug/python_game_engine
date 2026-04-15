from typing import *
from pathlib import Path
import time
import importlib
from importlib.util import spec_from_file_location, module_from_spec
from source.components.script import Script
import inspect
from api.script_behaviour import ScriptBehaviour
from source.logging import *


class ScriptSys:
    def __init__(self):
        self.script_components: list[Script] = []

    def is_registered(self, script: Script):
        if script in self.script_components:
            return True
        return False

    def add(self, script: Script):
        if not self.is_registered(script):
            self.script_components.append(script)

    def initialize_objects(self, objects : ScriptBehaviour, component: Script):
        objects.this = component
        objects.game_object = component.game_object
        objects.transform = component.game_object.transform

    def init_render(self):

        self.objects: list[ScriptBehaviour] = []
        for component in self.script_components:
            try:
                spec = spec_from_file_location(
                    str(component.file_path), str(component.file_path))

                if spec is None:
                    log_exception(
                        f"error: file <{component.file_path}> not find")

                try:
                    module = module_from_spec(spec)

                    spec.loader.exec_module(module)

                    for name, obj in module.__dict__.items():
                        if inspect.isclass(obj) and issubclass(obj, ScriptBehaviour) and obj is not ScriptBehaviour:
                            object = obj()
                            self.initialize_objects(object, component)
                            self.objects.append(object)

                except Exception as e:
                    log_exception(e)

            except (ModuleNotFoundError, ImportError):
                log_exception("module not found")

        for objects in self.objects:
            objects.start()

    def render(self, frame_info: "FrameInfo"):
        for objects in self.objects:
            objects.update()


class FrameInfo:
    """
    ### parameters for each frame:
    * start_time : Game started time
    * total_time : how much goes from start
    * last_time : last frame time setted
    * frames : frames count (can be used for index)
    * delta_time : each frames delta time
    * fps : game fps
    """

    def __init__(self):
        self.start_time = time.perf_counter()
        self.total_time = 0
        self.last_time = self.start_time
        self.frames = 0
        self.delta_time = 1
        self.fps = 0

    def update(self):
        now = time.perf_counter()
        self.delta_time = now - self.last_time
        self.fps =  1 / self.delta_time
        self.last_time = now
        self.total_time = self.last_time - self.start_time
        self.frames += 1
