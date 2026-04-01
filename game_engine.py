
from core import Core
from window import Window
from directx import DirectX

import time

class GameEngine:
    def __init__(self):
        
        # TODO: Handle Exception for window 
        self.directx_window = Window(500, 500)
        
        self.directx = DirectX(self.directx_window)
        
        self.core = Core(self.directx_window)
        

    def run_game(self):
    
        self.directx.clear_color(0xFFFF00FF)        
        self.directx.present()        


        for i in range(20000000):
            
            g = (
                250 - i,
                250 - i,
                i * 3,
                i * 3,
            )
            
            self.directx.fill_rect(*g, 0xFF0000FF)
            self.directx.present()
            time.sleep(0.3)
            
if __name__ == "__main__":
    game_engine = GameEngine()
    
    game_engine.run_game()
    
    