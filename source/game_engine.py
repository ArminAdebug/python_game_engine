import time
from PyQt6.QtCore import QTimer
from source.core.core import *
from source.raw_window import Window
from source.directx.directx import DirectX
from source.systems.render_sys import RenderSys
from source.object.scene import Scene, _SceneKey
from source.object.gameobject import GameObject
from source.systems.system_registery import Registery
from source.logging import *
from source.math import (
    Vector3
)

from source.components import (
    Component,
    Sprite,
    Transform,
)

# UpdateLoop = Callable[[list[Callable], Callable, FrameInfo], None]


class GameEngine:
    def __init__(self):

        # TODO: Handle Exception for window
        self.directx_window = Window(1920, 1080)
        self.loop_state = False
        self.directx = DirectX(self.directx_window.get_hwnd())

        self.core = Core(self.directx_window)

        # setup Systems
        self.render_sys = RenderSys(self.directx)

        self.system_dict = {
            "RenderSys": self.render_sys,
        }

        self.system_registery = Registery(self.system_dict)

        # test
        self.test_image = Sprite(
            r"F:\docc\armin\+Dev\Code\Python\3d test\w\yag.jpg", self.directx)

        self.test_scene = self.test()

    def blank_screen(self):
        self.directx.clear_color(0xFF000000)
        self.directx.present()

    def run_game(self, timer: QTimer):
        self.blank_screen()

        try:

            frame_info = FrameInfo()

            self.loop_state = True

            # updater(func_list, lambda : self.check_loop_state(timer), frame_info)


            try:

                timer.timeout.connect(lambda: self.update_loop(
                    self.system_dict,
                    lambda: self.check_loop_state(timer),
                    frame_info))

            except Exception as e:
                log_exception(repr(e))

            timer.start(50)  # 16 : ~60 FPS

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
        enemy = scene1.new_gameobject("enemy")

        sprite1 = Sprite(
            r"F:\docc\armin\+Dev\Code\Python\3d test\w\yag.jpg", self.directx)
        sprite2 = Sprite(
            r"F:\docc\armin\+Dev\Code\Python\3d test\w\galaxy.png", self.directx)

        player.add_component(sprite2)
        enemy.add_component(sprite1)

        player.get_component(Transform)[0].scale = Vector3(0.1, .1, 1)
        enemy.get_component(Transform)[0].scale = Vector3(0.1, 0.1, 1)
        enemy.get_component(Transform)[0].position = Vector3(50, 100, 0)


        return scene1

    def update_loop(self, systems: dict, exiting: Callable[[], bool], frame_info: FrameInfo) -> None:
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

            systems["RenderSys"].render()

            self.directx.end()
            self.directx.present()

        except Exception as e:
            log_exception(repr(e))
