"""
main module for handling loop and systems and scenes and other

"""
# pylint: disable=no-name-in-module

from typing import Callable

from PyQt6.QtCore import QTimer

from source.raw_window import Window
from source.directx.directx import DirectX
from source.object.scene import Scene, _SceneKey
from source.systems.system_registery import Registery
from source.logging import Logger
from source.asset.asset_manager import AssetManager
from source.components import (
    Script
)
from source.systems import (
    RenderSys,
    ScriptSys,
    script_sys
)
from api.api_wrapper import Wrapper


class GameEngine:
    """class of Engine for handling all important things
    """

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

        Wrapper.engine = self

    def blank_screen(self):
        """clear screen with solid black color and then present
        """
        self.directx.clear_color(0xFF000000)
        self.directx.present()

    def run_game(self, timer: QTimer):
        """
        runs game loop and start QTimer
        """
        self.blank_screen()

        # setup frame info
        frame_info = script_sys.FrameInfo()
        Wrapper.frame_info = frame_info

        self.loop_state = True

        try:

            timer.timeout.connect(lambda: self.update_loop(
                self.system_dict,
                lambda: self.check_loop_state(timer),
                frame_info))

        except (ValueError, TypeError, SyntaxError) as e:
            Logger.log_exception(repr(e))

        # setup systems
        try:
            self.system_dict["ScriptSys"].init_render()
            self.system_dict["RenderSys"].init_render()
        except (SyntaxError, KeyError, ValueError) as e:
            Logger.log_exception(e)

        timer.start(1)  # 16 : ~60 FPS
        self.blank_screen()

    def check_loop_state(self, timer):
        """checks loop state. if state was False it would stop loop

        Args:
            timer (_type_): current state of loop
        """

        if not self.loop_state:
            timer.stop()

    def new_scene(self, name: str) -> Scene:
        """use this to make a new scene.

        Args:
            name (str): name of new scene

        Returns:
            Scene: new Game scene
        """
        return Scene(name, _SceneKey, self.system_registery)

    def exit_loop(self):
        """this method set state of loop to False for check_loop_state stop loop
        """
        self.loop_state = False

    def test(self):
        """an test for testing game new logics.
        """

        scene1 = self.new_scene("game_play")
        player = scene1.new_gameobject("player")

        script1 = Script(
            r"F:\docc\armin\+Dev\Code\Python\3d test\w\test\test_script.py")

        player.add_component(script1)

    def update_loop(self,
                    systems: dict,
                    exiting: Callable[[], bool],
                    frame_info: script_sys.FrameInfo) -> None:
        """game play loop. looping with QTimer

        Args:
            systems (dict): main systems like RenderSys to run
            exiting (Callable): a Function for getting Exit status
            frame_info (FrameInfo): for update each frame data like deltatime and FPS
        """

        # this function will stop QTimer
        exiting()

        # start rendering
        self.directx.clear_color(0xFF000000)
        self.directx.begin()

        # rendering systems
        try:
            systems["ScriptSys"].render()
        except Exception as e:
            Logger.log_exception(repr(e))

        try:
            systems["RenderSys"].render()
        except Exception as e:
            Logger.log_exception(repr(e))

        # end rendering
        self.directx.end()
        self.directx.present()

        # update frame states
        frame_info.update()
        Wrapper.frame_info = frame_info
