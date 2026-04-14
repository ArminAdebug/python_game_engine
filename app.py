from PyQt6.QtWidgets import QApplication
import sys
from source.game_engine import *
import source.gui as gui

import faulthandler
faulthandler.enable()

def main():
    app = QApplication(sys.argv)

    game_engine = GameEngine()

    window = gui.Window(game_engine.directx_window.get_hwnd())

    window.ui.fun1.clicked.connect(lambda: game_engine.run_game(window.timer))

    window.ui.fun3.clicked.connect(game_engine.exit_loop)

    game_engine.blank_screen()

    app.exec()


if __name__ == "__main__":
    main()
