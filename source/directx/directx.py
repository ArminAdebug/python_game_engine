import ctypes
import numpy as np


class DirectX:
    def __init__(self, hwnd):
        self.dx9 = ctypes.WinDLL(
            r"F:\docc\armin\+Dev\Code\Python\3d test\w\source\directx\dxtools.dll")

        self.dx9.init_d3d9.argtypes = [ctypes.c_void_p]
        self.dx9.init_d3d9.restype = ctypes.c_long

        self.dx9.clear_color.argtypes = [ctypes.c_uint32]
        self.dx9.present.argtypes = []
        self.dx9.shutdown_d3d9.argtypes = []

        self.dx9.clear_color.argtypes = [ctypes.c_uint]
        self.dx9.clear_color.restype = ctypes.c_long

        self.dx9.fill_rect.argtypes = [
            ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
        self.dx9.fill_rect.restype = ctypes.c_long

        self.dx9.begin_scene.argtypes = []
        self.dx9.end_scene.argtypes = []

        self.hr = self.dx9.init_d3d9(hwnd)

        if self.hr != 0:
            raise OSError(f"DX init failed: {self.hr}")

        self.init_texture()

        self.test_texture = 0xFFFF00FF

    def begin(self):
        self.dx9.begin_scene()

    def end(self):
        self.dx9.end_scene()

    def init_texture(self):

        self.dx9.create_texture_argb.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]
        self.dx9.create_texture_argb.restype = ctypes.c_void_p

        self.dx9.draw_texture_rect.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float
        ]

    def clear_color(self, color):

        if self.hr != 0:
            raise OSError(f"init failed: {self.hr:#x}")

        self.dx9.clear_color(color)

    def fill_rect(self,
                  x: int,
                  y: int,
                  w: int,
                  h: int,
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

    # -------------------------

    def clear(self, color):
        self.dx9.clear_color(color)

    # -------------------------
    def present(self):
        self.dx9.present()

    # -------------------------
    def shutdown(self):
        self.dx9.shutdown_d3d9()

    # -------------------------
    def create_texture_from_argb(self, argb_2d: np.ndarray):
        if argb_2d.dtype != np.uint32:
            raise TypeError("expected uint32 ARGB data")

        h, w, c = argb_2d.shape
        pitch = argb_2d.strides[0]

        ptr = self.dx9.create_texture_argb(
            ctypes.c_void_p(argb_2d.ctypes.data),
            w, h, pitch
        )
        if not ptr:
            raise RuntimeError("texture creation failed")

        return ptr

    # -------------------------
    def draw_texture(self, tex, x, y, w, h):
        self.dx9.draw_texture_rect(
            id(self.test_texture),
            x,
            y,
            w,
            h
        )
