"""main app for starting app
"""
# pylint: disable=no-name-in-module

import sys
import faulthandler

from PyQt6.QtWidgets import QApplication

from source import gui
from source.game_engine import GameEngine


faulthandler.enable()


def main():
    """main function to start program
    """
    app = QApplication(sys.argv)

    game_engine = GameEngine()

    window = gui.Window(game_engine.directx_window.get_hwnd())

    window.ui.pushButton.clicked.connect(lambda: game_engine.run_game(window.timer))

    window.ui.pushButton_2.clicked.connect(game_engine.exit_loop)

    game_engine.blank_screen()

    app.exec()


if __name__ == "__main__":
    main()
