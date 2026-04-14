from PyQt6.QtCore import QTimer
from source.raw_window import Window
from source.directx.directx import DirectX
from source.object.scene import Scene, _SceneKey
from source.object.gameobject import GameObject
from source.systems.system_registery import Registery
from source.logging import *
from typing import *
from source.asset.asset_manager import AssetManager

from source.math import (
    Vector3,
    Quaternion
)

from source.components import (
    Component,
    Sprite,
    Transform,
    Script
)
from source.systems import (
    RenderSys,
    ScriptSys,
    script_sys
)
from api.api_wrapper import EngineWrapper


class GameEngine:
    def __init__(self):

        # TODO: Handle Exception for window
        self.directx_window = Window(1920, 1080)
        self.loop_state = False
        self.directx = DirectX(self.directx_window.get_hwnd())

        self.asset_manager = AssetManager(self.directx)

        # setup Systems
        self.render_sys = RenderSys(self.directx)
        self.script_sys = ScriptSys()

        self.system_dict = {
            "RenderSys": self.render_sys,
            "ScriptSys": self.script_sys
        }

        self.system_registery = Registery(self.system_dict)

        # test
        self.test()

        EngineWrapper.engine = self

    def blank_screen(self):
        self.directx.clear_color(0xFF000000)
        self.directx.present()

    def run_game(self, timer: QTimer):
        self.blank_screen()

        try:

            frame_info = script_sys.FrameInfo()

            self.loop_state = True

            # updater(func_list, lambda : self.check_loop_state(timer), frame_info)

            try:

                timer.timeout.connect(lambda: self.update_loop(
                    self.system_dict,
                    lambda: self.check_loop_state(timer),
                    frame_info))

            except Exception as e:
                log_exception(repr(e))

            # setup systems
            self.system_dict["ScriptSys"].init_render()
            self.system_dict["RenderSys"].init_render()

            timer.start(50)  # 16 : ~60 FPS
            self.blank_screen()

        except Exception as e:
            log_exception(repr(e))

    def check_loop_state(self, timer):
        if not self.loop_state:
            timer.stop()

    def new_scene(self, name) -> Scene:
        return Scene(name, _SceneKey, self.system_registery)

    def exit_loop(self):
        self.loop_state = False

    def test(self):

        scene1 = self.new_scene("game_play")
        player = scene1.new_gameobject("player")

        script1 = Script(
            r"F:\docc\armin\+Dev\Code\Python\3d test\w\test\test_script.py")

        player.add_component(script1)

    def update_loop(self, systems: dict, exiting: Callable[[], bool], frame_info: script_sys.FrameInfo) -> None:
        """game play loop. looping with QTimer

        Args:
            systems (dict): main systems like RenderSys to run
            exiting (Callable): a Function for getting Exit status
            frame_info (FrameInfo): for update each frame data like deltatime and FPS
        """

        try:
            # this function will stop QTimer
            exiting()

            self.directx.clear_color(0xFF000000)

            self.directx.begin()

            systems["ScriptSys"].render(frame_info)
            systems["RenderSys"].render()

            self.directx.end()
            self.directx.present()

        except Exception as e:
            log_exception(repr(e))
