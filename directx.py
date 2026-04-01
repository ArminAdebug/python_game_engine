from window import Window
import time

import comtypes
import comtypes.client

import ctypes
from ctypes import wintypes

class DirectX:
    def __init__(self, window : Window):
        self.dx9 = ctypes.WinDLL(r".\dxtools.dll")

        self.dx9.init_d3d9.argtypes = [ctypes.c_void_p]
        self.dx9.init_d3d9.restype = ctypes.c_long

        self.dx9.clear_color.argtypes = [ctypes.c_uint]
        self.dx9.clear_color.restype = ctypes.c_long

        self.dx9.fill_rect.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
        self.dx9.fill_rect.restype = ctypes.c_long

        self.dx9.present.argtypes = []
        self.dx9.present.restype = ctypes.c_long

        self.dx9.shutdown_d3d9.argtypes = []
        self.dx9.shutdown_d3d9.restype = None

        self.hwnd = window.get_hwnd()
        self.hr = self.dx9.init_d3d9(self.hwnd)
        
        
    def clear_color(self, color):
        
    
        if self.hr != 0:
            raise OSError(f"init failed: {self.hr:#x}")

        self.dx9.clear_color(color)
        
    def fill_rect(self,
                  x : int,
                  y : int,
                  w : int,
                  h : int,
                  color):
        """_summary_

        Args:
            x (int): rect x position
            y (int): rect y position
            w (int): rect width
            h (int): rect height
            color (_type_): rect color

        Raises:
            OSError: if directx init failed
        """
        
                
        if self.hr != 0:
            raise OSError(f"init failed: {self.hr:#x}")

        self.dx9.fill_rect(x, y, w, h, color) 

    def present(self):
        
        if self.hr != 0:
            raise OSError(f"init failed: {self.hr:#x}")
        
        self.dx9.present()

    def shutdown(self):
        self.dx9.shutdown_d3d9()        