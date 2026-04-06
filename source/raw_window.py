import ctypes
from ctypes import wintypes


class Window:

    WS_VISIBLE = 0x10000000
    WS_POPUP = 0x80000000

    user32 = ctypes.windll.user32

    def __init__(self, width, height):

        self.hwnd = Window.user32.CreateWindowExW(
            0,                       # dwExStyle
            "STATIC",                # lpClassName
            "",                      # lpWindowName  ← قبلاً اشتباهاً 100 گذاشته بودی
            Window.WS_POPUP | Window.WS_VISIBLE,  # dwStyle = WS_VISIBLE | WS_POPUP
            100, 100,                # X, Y
            width, height,           # nWidth, nHeight
            None, None,              # hWndParent, hMenu
            # hInstance (برای کلاس‌های سیستمی مثل STATIC می‌تونه None باشه)
            None,
            None                     # lpParam
        )

        if not self.hwnd:
            raise WindowsError("can't create window")

    def change_size(self, width, height):
        Window.user32.SetWindowPos(self.hwnd, 0, 0, 0, width, height, 0x0002)

    def get_hwnd(self):
        return self.hwnd
