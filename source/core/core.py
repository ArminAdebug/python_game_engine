from typing import Callable
from source.raw_window import Window
import time


class FrameInfo:
    """
    ### parameters for each frame:
    * start_time : Game started time
    * total_time : how much goes from start
    * last_time : last frame time setted
    * frames : frames count (can be used for index)
    * delta_time : each frames delta time
    """

    def __init__(self):
        self.start_time = time.perf_counter()
        self.total_time = 0
        self.last_time = self.start_time
        self.frames = 0
        self.delta_time = 1

    def update(self):
        self.delta_time = time.perf_counter() - self.last_time
        self.last_time = time.perf_counter()
        self.total_time = self.last_time - self.start_time
        self.frames += 1


UpdateLoop = Callable[[list[Callable], Callable, FrameInfo], None]


class Core:
    def __init__(self, dwindow: Window):
        self.directx_window = dwindow


if __name__ == "__main__":
    pass
