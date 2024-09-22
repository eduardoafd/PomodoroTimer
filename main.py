import sys

from PyQt5.QtCore import QSharedMemory
from PyQt5.QtWidgets import QApplication

from PomodoroTimerWindow import PomodoroTimerWindow
from PomodoroTrayIcon import PomodoroTrayIcon

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    shared_memory = QSharedMemory('PomodoroAppSharedMemoryKey')
    if not shared_memory.create(1):
        sys.exit(0)

    window = PomodoroTimerWindow()
    window.show()

    tray_icon = PomodoroTrayIcon()
    tray_icon.show()

    app.exec_()
