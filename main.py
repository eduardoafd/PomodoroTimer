import json
import os.path
import sys

from PyQt5.QtCore import QSharedMemory
from PyQt5.QtWidgets import QApplication

from PomodoroTimerWindow import PomodoroTimerWindow
from PomodoroTrayIcon import PomodoroTrayIcon

DEFAULT_SETUP = {
    'Work': 15,
    'Break': 5,
    'Rest': 15,
    'num_reps': 5
}

pomodoro_setup = None
if os.path.isfile('pomodoro_setup.json'):
    with open('pomodoro_setup.json', 'r') as f:
        pomodoro_setup = json.load(f)
else:
    try:
        json.dump(DEFAULT_SETUP, open('pomodoro_setup.json', 'w'))
        pomodoro_setup = DEFAULT_SETUP
    except Exception as e:
        print("Failed to save pomodoro_setup.json")
    else:
        pomodoro_setup = DEFAULT_SETUP
        print(f"Using Default setup {pomodoro_setup}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    shared_memory = QSharedMemory('PomodoroAppSharedMemoryKey')
    if not shared_memory.create(1):
        sys.exit(0)

    window = PomodoroTimerWindow(pomodoro_setup)
    window.show()

    tray_icon = PomodoroTrayIcon()
    tray_icon.show()

    def on_tray_icon_activated(reason):
        if reason == 2:
            window.show()

    tray_icon.quit_action.triggered.connect(app.quit)
    tray_icon.activated.connect(on_tray_icon_activated)

    window.timer_page.updateTime.connect(tray_icon.set_time)
    tray_icon.next_action.triggered.connect(window.timer_page.skip)
    tray_icon.pause_play_action.triggered.connect(window.timer_page.start_pause_button.click)
    window.timer_page.setPlayPause.connect(tray_icon.set_play_pause_text)
    tray_icon.timer_action.triggered.connect(window.show)

    app.exec_()
