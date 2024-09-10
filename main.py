import sys

from PyQt5.QtCore import QSharedMemory
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from PomodoroTrayIcon import PomodoroTrayIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 320)

        self.setWindowTitle('Pomodoro Timer')
        self.setWindowIcon(QIcon("./assets/tomato.ico"))




if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    shared_memory = QSharedMemory('MimrAppSharedMemoryKey')
    if not shared_memory.create(1):
        sys.exit(0)

    window = MainWindow()
    window.show()

    tray_icon = PomodoroTrayIcon()
    tray_icon.show()

    app.exec_()