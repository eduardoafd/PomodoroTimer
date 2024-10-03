from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction


class PomodoroTrayIcon(QSystemTrayIcon):
    def __init__(self):

        super(PomodoroTrayIcon, self).__init__()

        self.setIcon(QIcon("./assets/tomato.svg"))
        self.setVisible(True)

        self.menu= QMenu()

        self.timer_action = QAction("Open Timer")
        self.timer_status = QAction("Work: 00:00:00")
        self.timer_status.setEnabled(False)

        self.pause_play_action = QAction("Play")

        self.next_action = QAction("Next")

        self.quit_action = QAction("Quit")

        self.menu.addAction(self.timer_action)
        self.menu.addSeparator()
        self.menu.addAction(self.timer_status)
        self.menu.addAction(self.pause_play_action)
        self.menu.addAction(self.next_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)

    def set_time(self, update):
        state, time = update
        if time >= 0:
            minutes = time // 60
            remaining_seconds = time % 60

            self.timer_status.setText(f"{state}: {minutes:02}:{remaining_seconds:02}")
        else:
            pass

    def set_play_pause_text(self, text):
        self.pause_play_action.setText(text)

