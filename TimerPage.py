from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QSize, QPropertyAnimation, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QSizePolicy, QHBoxLayout, QGraphicsOpacityEffect


class Timer(QTimer):
    timeout_signal = pyqtSignal()
    tick = pyqtSignal(int)

    def __init__(self, duration, play_sound_when_finished=True):
        super().__init__()
        self.duration = duration
        self.remaining_time = duration
        self.isActive = False

        self.player = QMediaPlayer()
        self.sound_file = './assets/hotel-bell-ding-1-174457.mp3'
        self.play_sound_when_finished = play_sound_when_finished

        self.timeout.connect(self.update)

    def set_duration(self, duration):
        self.duration = duration
        self.remaining_time = duration

    def update(self):
        self.tick.emit(int(self.remaining_time))
        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            self.stop(emit=False)
            if self.play_sound_when_finished:
                url = QUrl.fromLocalFile(self.sound_file)
                content = QMediaContent(url)
                self.player.setMedia(content)
                self.player.setVolume(100)
                self.player.play()

            self.timeout_signal.emit()

    def start(self):
        if not self.isActive:
            super().start(1000)
            self.isActive = True

    def pause(self):
        if self.isActive:
            super().stop()
            self.isActive = False

    def stop(self, emit=True):
        super().stop()

        if self.isActive:
            self.remaining_time = self.duration
            self.isActive = False

            if emit:
                self.timeout_signal.emit()

    def get_remaining_time(self, format_str=False):
        if format_str:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            return f"{minutes:02}:{seconds:02}"
        else:
            return self.remaining_time


class PomodoroStateSelector(QFrame):
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


class FadeButton(QPushButton):
    def __init__(self, normal_icon, hover_icon, parent=None):
        super().__init__(parent)

        self.setIconSize(QSize(60, 60))
        self.setStyleSheet("background-color: transparent;")

        self.normal_icon = normal_icon
        self.hover_icon = hover_icon
        self.setIcon(self.normal_icon)

        self.setCursor(Qt.PointingHandCursor)

        self.fade_out()

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.normal_icon)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.fade_out()
        super().mousePressEvent(event)

    def fade_out(self):
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

        QTimer.singleShot(250, self.hide)

    def show(self):
        super().show()

        QTimer.singleShot(50, self.unfade)

    def unfade(self):
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()


class TimerPage(QFrame):
    def __init__(self, work_duration_min=25, rest_duration_min=5, break_duration_min=15, num_reps= 5, parent=None):
        super().__init__(parent)
        self.setFixedSize(480, 320)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background: #E74C3C; padding: 0px;")

        self.current_state = 'Work'
        self.reps_counter = 0

        self.work_duration = work_duration_min * 60
        self.break_duration = break_duration_min * 60
        self.rest_duration = rest_duration_min * 60
        self.num_repetitions = num_reps

        self.work_timer = Timer(duration=self.work_duration)
        self.work_timer.tick.connect(self.set_time)
        self.work_timer.timeout_signal.connect(self.work_finished)

        self.break_timer = Timer(duration=self.break_duration)
        self.break_timer.tick.connect(self.set_time)
        self.break_timer.timeout_signal.connect(lambda: self.pomodoro_states.select_option('Work'))

        self.rest_timer = Timer(duration=self.rest_duration)
        self.rest_timer.tick.connect(self.set_time)
        self.rest_timer.timeout_signal.connect(self.long_rest_finished)

        self.timers = {
            "Work": self.work_timer,
            "Break": self.break_timer,
            "Rest": self.rest_timer,
        }

        self.timer_display = QLabel()
        self.timer_display.setStyleSheet(
            "font-family: Inter; font-size: 120px; color: #ECF0F1; padding: 0px; align: center;")
        self.timer_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.timer_display.setAlignment(Qt.AlignCenter)

        self.start_pause_button = QPushButton("Start")
        self.start_pause_button.clicked.connect(self._on_button_click)
        self.start_pause_button.setStyleSheet("""
            QPushButton {
                background: #ECF0F1;
                font-family: Inter;
                font-size: 28px;
                color: #E74C3C;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #D5DBDB;  /* Change to a lighter color on hover */
                color: #C0392B;       /* Darker text color on hover */
            }
            QPushButton:pressed {
                background: #BDC3C7;  /* Change to a darker color when pressed */
                color: #A93226;       /* Darker text color when pressed */
            }
            QPushButton[customState="Work"] {
                color: #E74C3C;
            }
        
            QPushButton[customState="Break"] {
                color: #34495E;
            }
        
            QPushButton[customState="Rest"] {
                color: #1ABC9C;
            }
        """)
        self.start_pause_button.setFixedSize(120, 60)
        self.start_pause_button.setCursor(Qt.PointingHandCursor)
        self.start_pause_button.setProperty('customState', 'Work')
        self.start_pause_button.style().unpolish(self.start_pause_button)
        self.start_pause_button.style().polish(self.start_pause_button)

        self.pomodoro_states = PomodoroStateSelector()
        self.pomodoro_states.selectionChanged.connect(self.set_state)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.pomodoro_states, alignment=Qt.AlignHCenter)
        layout.addWidget(self.timer_display)
        layout.addWidget(self.start_pause_button, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

        self.settings_button = QPushButton(self)
        self.settings_button.setFixedSize(60, 60)
        # background: #B70F0F;
        self.settings_button.setStyleSheet("""
            QPushButton {
                border-radius: 30px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background: rgba(0, 0, 0, 0.1);
            }
        """)
        self.settings_button.setIcon(QIcon("./assets/chef-hat.svg"))
        self.settings_button.setIconSize(QSize(40, 40))
        self.settings_button.setCursor(Qt.PointingHandCursor)

        self.skip_button = FadeButton(QIcon("./assets/cutelo.svg"), QIcon("./assets/cutelo-hover.svg"), parent=self)
        self.skip_button.clicked.connect(self.skip)

        self.reps_counter_label = QLabel(f"{self.reps_counter}x", parent=self)
        self.reps_counter_label.setStyleSheet("font-family: Inter; font-size: 24px; color: #ECF0F1; padding: 0px;")

        self.set_time(self.work_duration)

    def resizeEvent(self, event):
        self.settings_button.move(self.width() - self.settings_button.width() - 20,
                                  20)

        self.skip_button.move(self.start_pause_button.x() + self.start_pause_button.width() + 20,
                              self.start_pause_button.y() + (
                                          self.start_pause_button.height() - self.skip_button.height()) // 2)

        self.reps_counter_label.move(20,
                                     self.height() - self.reps_counter_label.height() - 20)

        super().resizeEvent(event)

    def work_finished(self):
        self.reps_counter += 1
        self.reps_counter_label.setText(f"{self.reps_counter}x")
        self.pomodoro_states.select_option('Break' if self.reps_counter < self.num_repetitions else 'Rest')

    def long_rest_finished(self):
        self.reps_counter = 0
        self.pomodoro_states.select_option('Work')

    def set_time(self, seconds):
        if seconds >= 0:
            minutes = seconds // 60
            remaining_seconds = seconds % 60

            self.timer_display.setText(f"{minutes:02}:{remaining_seconds:02}")
        else:
            self.timer_display.setText(f"00:00")

    def _on_button_click(self):
        timer = self.timers[self.current_state]
        if timer.isActive:
            timer.pause()
            self.start_pause_button.setText('Start')
            self.skip_button.fade_out()
        else:
            timer.start()
            self.start_pause_button.setText('Pause')
            self.skip_button.show()

    def skip(self):
        if self.current_state == 'Work':
            self.work_finished()

        elif self.current_state == 'Break':
            self.pomodoro_states.select_option('Work')

        elif self.current_state == 'Rest':
            self.pomodoro_states.select_option('Work')

    def set_state(self, state):
        self.current_state = state

        self.work_timer.stop(emit=False)
        self.break_timer.stop(emit=False)
        self.rest_timer.stop(emit=False)

        if self.current_state == 'Work':
            self.setStyleSheet("background: #E74C3C; padding: 0px;")
            self.set_time(self.work_duration)
            self.start_pause_button.setProperty('customState', 'Work')

        if self.current_state == 'Break':
            self.setStyleSheet("background: #34495E; padding: 0px;")
            self.set_time(self.break_duration)
            self.start_pause_button.setProperty('customState', 'Break')

        if self.current_state == 'Rest':
            self.setStyleSheet("background: #1ABC9C; padding: 0px;")
            self.set_time(self.rest_duration)
            self.reps_counter = 0
            self.reps_counter_label.setText(f"{self.reps_counter}x")
            self.start_pause_button.setProperty('customState', 'Rest')

        self.start_pause_button.style().unpolish(self.start_pause_button)
        self.start_pause_button.style().polish(self.start_pause_button)

        self.start_pause_button.setText('Start')
        self.skip_button.fade_out()

        self.update()

    def set_work_duration(self, duration_min):
        self.work_duration = duration_min * 60
        self.work_timer.set_duration(self.work_duration)
        if self.current_state == 'Work' and not self.work_timer.isActive:
            self.set_time(self.work_duration)

    def set_break_duration(self, duration_min):
        self.break_duration = duration_min * 60
        self.break_timer.set_duration(self.break_duration)
        if self.current_state == 'Break' and not self.break_timer.isActive:
            self.set_time(self.break_duration)

    def set_rest_duration(self, duration_min):
        self.rest_duration = duration_min * 60
        self.rest_timer.set_duration(self.rest_duration)
        if self.current_state == 'Rest' and not self.rest_timer.isActive:
            self.set_time(self.rest_duration)
