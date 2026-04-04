from source.utility.helper import *
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
    def __init__(self, dwindow : Window):
        self.directx_window = dwindow
    
    def get_loop_update(self, funcs : list) -> UpdateLoop:
        """_summary_

        Args:
            funcs (list): functions to run in loop
            exiting (func): funcs must be a function and if exiting return True loop will end.

        Returns:
            int: loop exit status
        """

        for func in funcs:
            if not isinstance(func, Callable):
                raise ValueError("Some things on this list are not Function")

        
        def update_loop(funcs : list[Callable], exiting : Callable, frame_info : FrameInfo) -> None:


            # this function will stop QTimer
            exiting()

            for func in funcs:
                try:
                    func()
                    
                except Exception as e:
                    print(e)

                   
        return update_loop

    
