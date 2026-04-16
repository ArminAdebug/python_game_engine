import ctypes
import numpy as np
from source.logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from source.math import Vector3


class DirectX:
    dll_path = str(Path(r".\source\directx\dxtools.dll").absolute())

    def __init__(self, hwnd: int):
        """create directx wrapper

        Args:
            hwnd (int): an raw window poinet to draw

        Raises:
            OSError: if init failed
        """
        try:
            if not os.path.exists(__class__.dll_path):
                Logger.log_error(f"file {__class__.dll_path} does not exists")

            self.dx9 = ctypes.WinDLL(
                __class__.dll_path
            )

            self.dx9.init_d3d9.argtypes = [ctypes.c_void_p]
            self.dx9.init_d3d9.restype = ctypes.c_long

        except (FileExistsError,
                OSError,
                FileExistsError,
                ctypes.ArgumentError,
                ) as e:

            Logger.log_exception(repr(e))

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

    def begin(self):
        self.dx9.begin_scene()

    def end(self):
        self.dx9.end_scene()

    def init_texture(self):
        """setup texture setting
        """

        try:
            self.dx9.create_texture_grba.argtypes = [
                ctypes.c_void_p,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int
            ]
            self.dx9.create_texture_grba.restype = ctypes.c_void_p

            self.dx9.draw_texture_rect.argtypes = [
                ctypes.c_void_p,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
                ctypes.c_float,
            ]
        except Exception as e:
            Logger.log_exception(repr(e))

    def clear_color(self, color: int):
        """clear color with a color.

        Args:
            color (int): rgb hex color.

        Raises:
            OSError: if init was failed.
        """
        if self.hr != 0:
            raise OSError(f"init failed: {self.hr:#x}")

        self.dx9.clear_color(color)

    def fill_rect(self,
                  x: int,
                  y: int,
                  w: int,
                  h: int,
                  color: int):
        """draws a rect with position and size and color

        Args:
            x (int): rect x position
            y (int): rect y position
            w (int): rect width
            h (int): rect height
            color (int): rect hex color

        Raises:
            OSError: if directx init failed
        """

        if self.hr != 0:
            raise OSError(f"init failed: {self.hr:#x}")

        self.dx9.fill_rect(x, y, w, h, color)

    # -------------------------
    def present(self):
        self.dx9.present()

    # -------------------------
    def shutdown(self):
        self.dx9.shutdown_d3d9()

    # -------------------------
    def create_texture_from_grba(self, grba_2d: np.ndarray) -> int:
        """creates texture from numpy array grba.

        Args:
            grba_2d (np.ndarray): numpy array from image mode grba

        Raises:
            TypeError: if numpy type was Wrong
            RuntimeError: if texture creation failed

        Returns:
            int: pointer to texture
        """
        if grba_2d.dtype != np.uint8:
            raise TypeError("expected uint8 grba data")

        h, w, _ = grba_2d.shape
        pitch = grba_2d.strides[0]

        ptr = self.dx9.create_texture_grba(
            ctypes.c_void_p(grba_2d.ctypes.data),
            w, h, pitch
        )

        if not ptr:
            raise RuntimeError(f"texture creation failed {ptr=}")

        return ptr

    # -------------------------
    def draw_texture(self,
                     tex: int,
                     position0: "Vector3",
                     position1: "Vector3",
                     position2: "Vector3",
                     position3: "Vector3"
                     ):
        """draws an texture on screen

        Args:
            tex (int): texture pointer
            position0 (Vector3): vertex 1 position
            position1 (Vector3): vertex 2 position
            position2 (Vector3): vertex 3 position
            position3 (Vector3): vertex 4 position
        """

        try:
            self.dx9.draw_texture_rect(
                tex,
                position0.x, position0.y, position0.z,
                position1.x, position1.y, position1.z,
                position2.x, position2.y, position2.z,
                position3.x, position3.y, position3.z
            )
        except (ctypes.ArgumentError, OSError, WindowsError) as e:
            Logger.log_exception(repr(e))
