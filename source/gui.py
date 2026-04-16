# pylint: disable=no-name-in-module

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QMenu, QLayout

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

        container = QWidget.createWindowContainer(directx_window)

        layout = QVBoxLayout(self.ui.screen)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

        self.timer = QTimer()

        self.show()
        self.setupAddComponent()

    def setupAddComponent(self):
        """connecting button to components list
        """
        menu = QMenu(self)

        # اضافه کردن کامپوننت‌ها
        menu.addAction("Transform")
        menu.addAction("Mesh Renderer")
        menu.addAction("Box Collider")
        menu.addAction("Rigidbody")

        #self.ui.clicked.connect(
        #    lambda: menu.exec(
        #        self.btnAddComponent.mapToGlobal(
        #            self.btnAddComponent.rect().bottomLeft()
        #        )
        #    )
        #)

    def _delete_layout(self, layout : QLayout):
        layout.deleteLater()
