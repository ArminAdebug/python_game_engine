"""main app for starting app
"""
# pylint: disable=no-name-in-module

import sys
import faulthandler

from PyQt6.QtWidgets import QApplication

from source.gui.window import Window
from source.game_engine import GameEngine


faulthandler.enable()


def main():
    """main function to start program"""

    app = QApplication(sys.argv)

    game_engine = GameEngine()

    window = Window(game_engine)

    app.exec()


if __name__ == "__main__":
    main()
