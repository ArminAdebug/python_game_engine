
from source.core import *
from source.raw_window import Window
from source.directx.directx import DirectX
from PyQt6.QtWidgets import QMainWindow
import time

from source.component import (
    component,
    sprite,
)

# UpdateLoop = Callable[[list[Callable], Callable, FrameInfo], None]


class GameEngine:
    def __init__(self):

        # TODO: Handle Exception for window
        self.directx_window = Window(500, 500)
        self.loop_state = False
        self.directx = DirectX(self.directx_window.get_hwnd())

        self.core = Core(self.directx_window)

    def blank_screen(self):
        self.directx.clear_color(0xFF000000)
        self.directx.present()

    def run_game(self, timer):
        self.blank_screen()

        func_list = self.get_func_list()

        frame_info = FrameInfo()

        updater = self.core.get_loop_update(func_list)

        try:

            self.loop_state = True

            # updater(func_list, lambda : self.check_loop_state(timer), frame_info)

            try:

                timer.timeout.connect(lambda: updater(
                    func_list, lambda: self.check_loop_state(timer), frame_info))

            except Exception as e:
                print(e)

            timer.start(50)  # 16 : ~60 FPS

        except Exception as e:
            print(repr(e))

    def check_loop_state(self, timer):
        if not self.loop_state:
            timer.stop()

    def exit_loop(self):
        self.loop_state = False

    def get_func_list(self):
        return [
            self.test_animation,

        ]

    def test_animation(self):
        try:
            self.directx.begin()

            self.directx.clear_color(0xFF202020)


            self.directx.fill_rect(50, 50, 200, 200, 0xFFFF0000)

            image = sprite.Sprite(
                r"F:\docc\armin\+Dev\Code\Python\3d test\w\test.png", self.directx)
            print(f"{image.texture=}")
            self.directx.draw_texture(image.texture, 0, 0, 256, 256)

            self.directx.end()
            self.directx.present()

        except Exception as e:
            print(repr(e))
