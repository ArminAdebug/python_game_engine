from PyQt6.QtCore import QBasicTimer

def wr():
    def main(inp : int) -> bool:
        return inp % 2 == 0

    return main

QBasicTimer.wrt = wr

b = QBasicTimer


