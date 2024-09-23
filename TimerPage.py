from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QSizePolicy, QHBoxLayout


class Timer(QTimer):
    timeout_signal = pyqtSignal()
    tick = pyqtSignal(int)

    def __init__(self, duration):
        super().__init__()
        self.duration = duration
        self.remaining_time = duration
        self.isActive = False

        self.timeout.connect(self.update)

    def set_duration(self, duration):
        self.duration = duration
        self.remaining_time = duration

    def update(self):
        self.tick.emit(int(self.remaining_time))
        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            self.stop()
            self.timeout_signal.emit()

    def start(self):
        if not self.isActive:
            super().start(1000)
            self.isActive = True

    def pause(self):
        if self.isActive:
            super().stop()
            self.isActive = False

    def stop(self):
        super().stop()
        self.remaining_time = self.duration
        self.isActive = False

    def get_remaining_time(self, format_str=False):
        if format_str:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            return f"{minutes:02}:{seconds:02}"
        else:
            return self.remaining_time


class PomodoroStates(QFrame):
    selectionChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setContentsMargins(0, 0, 0, 0)

        btn_style = """
            QPushButton {
                border: none;
                background: transparent;
                font-size: 24px;
                color: #ECF0F1;
                padding: 10px;
            }
            QPushButton:checked {
                border-bottom: 2px solid #ECF0F1;
            }
        """

        self.buttons = {
            "Work": QPushButton("Work"),
            "Break": QPushButton("Break"),
            "Rest": QPushButton("Rest"),
        }

        for btn_text, button in self.buttons.items():
            button.setCheckable(True)
            button.setStyleSheet(btn_style)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda _, text=btn_text: self.select_option(text))

        self.buttons["Work"].setChecked(True)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        for button in self.buttons.values():
            layout.addWidget(button)

        self.setLayout(layout)

    def select_option(self, option):
        for button in self.buttons.values():
            button.setChecked(False)

        self.buttons[option].setChecked(True)

        self.selectionChanged.emit(option)


class TimerPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(20, 20, 20, 20)

        self.setFixedSize(480, 320)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background: #E74C3C; padding: 0px;")

        self.states = {
            'work': 0,
            'rest': 1,
            'long_rest': 2,
        }
        self.current_state = self.states['work']
        self.reps_counter = 0

        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.rest_duration = 15 * 60
        self.num_repetitions = 5

        self.work_timer = Timer(duration=self.work_duration)
        self.work_timer.tick.connect(self.set_time)

        self.rest_timer = Timer(duration=self.break_duration)
        self.rest_timer.tick.connect(self.set_time)

        self.long_rest_timer = Timer(duration=self.rest_duration)
        self.long_rest_timer.tick.connect(self.set_time)

        self.timer_display = QLabel()
        self.timer_display.setStyleSheet(
            "font-family: Inter; font-size: 120px; color: #ECF0F1; padding: 0px; align: center;")
        self.timer_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.timer_display.setAlignment(Qt.AlignCenter)

        self.start_pause_button = QPushButton("Start")
        self.start_pause_button.clicked.connect(self._on_button_click)
        self.start_pause_button.setStyleSheet(
            "background: #ECF0F1; font-family: Inter; font-size: 28px; color: #E74C3C; border-radius: 8px;")
        self.start_pause_button.setFixedSize(120, 60)
        self.start_pause_button.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # layout.addWidget(self.settings_button, alignment=Qt.AlignRight)
        layout.addWidget(PomodoroStates(), alignment=Qt.AlignHCenter)
        layout.addWidget(self.timer_display)
        layout.addWidget(self.start_pause_button, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

        self.settings_button = QPushButton()
        self.settings_button.setFixedSize(60, 60)
        self.settings_button.setStyleSheet(
            "QPushButton {"
            "border-radius: 30px;"
            "}"
            "QPushButton:hover {"
            "background: #B70F0F;"
            "}"
            "QPushButton:pressed {"
            "background: #9C0D0D;"
            "}")
        self.settings_button.setIcon(QIcon("./assets/menu.svg"))
        self.settings_button.setIconSize(QSize(40, 40))
        self.settings_button.setCursor(Qt.PointingHandCursor)

        self.set_time(self.work_duration)

    def set_time(self, seconds):
        if seconds >= 0:
            minutes = seconds // 60
            remaining_seconds = seconds % 60

            self.timer_display.setText(f"{minutes:02}:{remaining_seconds:02}")
        else:
            self.timer_display.setText(f"00:00")

    def _on_button_click(self):
        if self.work_timer.isActive:
            self.work_timer.pause()
            self.start_pause_button.setText('Start')
        else:
            self.work_timer.start()
            self.start_pause_button.setText('Pause')
