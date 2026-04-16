"""system for running user code
"""

import time
import os
import inspect

from importlib.util import spec_from_file_location, module_from_spec

from source.components.script import Script
from api.script_behaviour import ScriptBehaviour
from source.logging import Logger


class ScriptSys:
    """system for running user code
    """

    def __init__(self):
        self.script_components: list[Script] = []
        self.objects: list[ScriptBehaviour] = []

    def is_registered(self, script: Script) -> bool:
        """returns True if commponent already regestered

        Args:
            script (Script): component to check

        Returns:
            bool: registeration state
        """

        if script in self.script_components:
            return True
        return False

    def add(self, script: Script):
        """add script Component to system

        Args:
            script (Script): commponent to add
        """
        if not self.is_registered(script):
            self.script_components.append(script)

    def initialize_objects(self, objects: ScriptBehaviour, component: Script):
        """inject statics to user code object

        Args:
            objects (ScriptBehaviour): object of user code class
            component (Script): Script component of user code
        """

        objects.this = component
        objects.game_object = component.game_object
        objects.transform = component.game_object.transform

    def init_render(self):
        """setup for Script system
        finds script class and setup them for rendering.
        """

        for component in self.script_components:

            if not os.path.exists(component.file_path):
                Logger.log_error(
                    f"File Doesn't exists : <{component.file_path}>")

            try:
                spec = spec_from_file_location(
                    str(component.file_path), str(component.file_path))

                if spec is None:
                    Logger.log_exception(
                        f"error: file <{component.file_path}> not find")
                    continue

                module = module_from_spec(spec)

                spec.loader.exec_module(module)

            except (ModuleNotFoundError, ImportError):
                Logger.log_exception("module not found")

            try:
                for _, obj in module.__dict__.items():
                    if inspect.isclass(obj) and issubclass(obj, ScriptBehaviour) and obj is not ScriptBehaviour:
                        script_object = obj()
                        self.initialize_objects(script_object, component)
                        self.objects.append(script_object)
            except (AttributeError, TypeError, ValueError, NameError) as e:
                Logger.log_exception(e)

        # run user starts methods
        for obj in self.objects:
            obj.start()

    def render(self):
        """runs user update method in main loop
        """

        for obj in self.objects:
            obj.update()


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
        """setup values
        """
        self.start_time = time.perf_counter()
        self.total_time = 0
        self.last_time = self.start_time
        self.frames = 0
        self.delta_time = 1
        self.fps = 0

    def update(self):
        """update values
        """
        now = time.perf_counter()
        self.delta_time = now - self.last_time
        self.fps = 1 / self.delta_time
        self.last_time = now
        self.total_time = self.last_time - self.start_time
        self.frames += 1
