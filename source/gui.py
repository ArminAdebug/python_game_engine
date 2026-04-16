# pylint: disable=no-name-in-module

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMainWindow

from source.window_ui import Ui_MainWindow


class Window(QMainWindow):
    """app main window and GUI
    """

    def __init__(self, directx_hwnd: int):
        """setup app GUI

        Args:
            directx_hwnd (int): pointer of an raw window
        """

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        directx_window = QWindow.fromWinId(directx_hwnd)

        directx_window = QWindow.fromWinId(directx_hwnd)

        # ساخت container
        container = QWidget.createWindowContainer(directx_window)

        # layout روی widget داخل UI
        layout = QVBoxLayout(self.ui.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

        self.timer = QTimer()

        self.show()
