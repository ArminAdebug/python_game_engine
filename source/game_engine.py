
from source.core import *
from source.raw_window import Window
from source.directx.directx import DirectX
from PyQt6.QtWidgets import QMainWindow
import time


#UpdateLoop = Callable[[list[Callable], Callable, FrameInfo], None]

class GameEngine:
    def __init__(self):
        
        # TODO: Handle Exception for window 
        self.directx_window = Window(500, 500)
        self.loop_state = False
        self.directx = DirectX(self.directx_window)
        
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
                       
            #updater(func_list, lambda : self.check_loop_state(timer), frame_info)
            
            try:

                timer.timeout.connect(lambda : updater(func_list, lambda : self.check_loop_state(timer), frame_info))

            except Exception as e:
                print(e)
                

            timer.start(16) # ~60 FPS
            
        except Exception as e:
            print(repr(e))
            
    def check_loop_state(self, timer):
        if not self.loop_state:
            timer.stop()
            
    def exit_loop(self):
        self.loop_state = False
        
    def get_func_list(self):
        return [
            self.code_player,
               
        ]
            
    def code_player(self):
        try:
            self.directx.clear_color(0xFFFF00FF)        
            import random
            
            w = random.randint(1, 200)
            h = random.randint(1, 200)
            
            g = (
                int(250 - (w / 2)),
                int(250 - (h / 2)),
                w,
                h,
            )
            
            self.directx.fill_rect(*g, 0xFF0000FF)
            self.directx.present()
            
        except Exception as e:
            print(e)
            
