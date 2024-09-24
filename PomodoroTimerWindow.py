from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFrame

from SetupPage import SetupPage
from TimerPage import TimerPage


class PomodoroTimerWindow(QMainWindow):
    def __init__(self, setup):
        super().__init__()
        self.setFixedSize(480, 320)

        self.setWindowTitle('Pomodoro Timer')
        self.setWindowIcon(QIcon("./assets/tomato.svg"))

        self.setStyleSheet("background: #E74C3C;")

        self.pages = QStackedWidget()

        self.timer_page = TimerPage(
            work_duration_min=setup.get('Work', 25),
            break_duration_min=setup.get('Break', 5),
            rest_duration_min=setup.get('Rest', 15),
            num_reps=setup.get('num_reps', 5)
        )

        self.timer_page.work_timer.timeout_signal.connect(self.show)
        self.timer_page.break_timer.timeout_signal.connect(self.show)
        self.timer_page.rest_timer.timeout_signal.connect(self.show)

        self.setup_page = SetupPage(
            work_duration_min=setup.get('Work', 25),
            break_duration_min=setup.get('Break', 5),
            rest_duration_min=setup.get('Rest', 15),
            num_reps=setup.get('num_reps', 5)
        )

        self.pages.addWidget(self.timer_page)
        self.pages.addWidget(self.setup_page)

        self.pages.setCurrentIndex(1)

        self.layout().addWidget(self.pages)
        self.layout().setAlignment(Qt.AlignCenter)

        self.timer_page.settings_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.setup_page.return_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))

        self.setup_page.work_time_selector.slider.valueChanged.connect(self.timer_page.set_work_duration)
        self.setup_page.break_time_selector.slider.valueChanged.connect(self.timer_page.set_break_duration)
        self.setup_page.rest_time_selector.slider.valueChanged.connect(self.timer_page.set_rest_duration)