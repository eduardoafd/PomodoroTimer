from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFrame

from TimerPage import TimerPage


class PomodoroTimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 320)

        self.setWindowTitle('Pomodoro Timer')
        self.setWindowIcon(QIcon("./assets/tomato.svg"))

        self.setStyleSheet("background: #E74C3C;")

        self.pages = QStackedWidget()

        self.timer_page = TimerPage()

        self.setup_page = QFrame()
        self.setup_page.setStyleSheet("background: #006311;")

        self.pages.addWidget(self.timer_page)
        self.pages.addWidget(self.setup_page)

        # self.pages.setCurrentIndex(1)

        self.layout().addWidget(self.pages)
        self.layout().setAlignment(Qt.AlignCenter)

        self.timer_page.settings_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))
