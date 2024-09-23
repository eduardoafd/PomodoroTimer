from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFrame

from SetupPage import SetupPage
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
        self.timer_page.work_timer.timeout_signal.connect(self.show)
        self.timer_page.break_timer.timeout_signal.connect(self.show)
        self.timer_page.rest_timer.timeout_signal.connect(self.show)

        self.setup_page = SetupPage()

        self.pages.addWidget(self.timer_page)
        self.pages.addWidget(self.setup_page)

        self.layout().addWidget(self.pages)
        self.layout().setAlignment(Qt.AlignCenter)

        self.timer_page.settings_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))

        self.pages.setCurrentIndex(1)