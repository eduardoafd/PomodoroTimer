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
        self.pause_play_action = QAction("Pause/Play")
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


