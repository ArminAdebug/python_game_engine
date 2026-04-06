from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import sys
from source.game_engine import *

import source.gui as gui


def main():
    app = QApplication(sys.argv)

    game_engine = GameEngine()

    s = sprite.Sprite(
        r"F:\docc\armin\+Dev\Code\Python\3d test\w\test.png", game_engine.directx)

    print(s.pixel_array)

    window = gui.Window(game_engine.directx_window.get_hwnd())

    window.ui.fun1.clicked.connect(lambda: game_engine.run_game(window.timer))

    window.ui.fun3.clicked.connect(game_engine.exit_loop)

    game_engine.blank_screen()

    app.exec()


if __name__ == "__main__":
    main()
