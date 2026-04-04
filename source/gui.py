from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QWidget, QMainWindow
from source.window_ui import Ui_MainWindow
from PyQt6.QtCore import QTimer



class Window(QMainWindow):
    def __init__(self, directx_hwnd):
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
        