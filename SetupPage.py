from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QPushButton, QSizePolicy, QLabel, QSlider, QHBoxLayout, QVBoxLayout

slider_styleSheet = """
QWidget {
    background: transparent;
}

QSlider:horizontal {
    min-height: 60px;
}
QSlider::groove:horizontal {
    height: 1px;
    background: white; 
}
QSlider::handle:horizontal {
    width: 30px;
    margin-top: -15px;
    margin-bottom: -15px;
    border-radius: 15px;
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(210, 210, 210, 255), stop:0.7 rgba(210, 210, 210, 100));
}
QSlider::handle:horizontal:hover {
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(255, 255, 255, 255), stop:0.7 rgba(255, 255, 255, 100));
}

QSlider:vertical {
    min-width: 60px;
}
QSlider::groove:vertical {
    width: 1px;
    background: white; 
}
QSlider::handle:vertical {
    height: 30px;
    margin-left: -15px;
    margin-right: -15px;
    border-radius: 15px;
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(210, 210, 210, 255), stop:0.7 rgba(210, 210, 210, 100));
}
QSlider::handle:vertical:hover {
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(255, 255, 255, 255), stop:0.7 rgba(255, 255, 255, 100));
}
"""

class TimerSelector(QFrame):
    def __init__(self, title:str, value: int, min_value: int, max_value: int, parent=None):
        super().__init__(parent=parent)
        # self.setStyleSheet('background: #656565;')
        self.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.title = QLabel(title)
        self.title.setStyleSheet("font-family: Inter; font-size: 24px; color: #ECF0F1; padding: 0px;")


        self.value_label = QLabel(f"{value} min")
        self.value_label.setStyleSheet("font-family: Inter; font-size: 18px; color: #ECF0F1; padding: 0px;")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setTickInterval(1)
        self.slider.setValue(value)
        self.slider.setFixedWidth(380)

        self.slider.valueChanged.connect(lambda val: self.value_label.setText(f"{val} min"))

        self.slider.setStyleSheet(slider_styleSheet)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(24)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(self.slider)
        h_layout.addWidget(self.value_label)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setSpacing(0)
        layout.addWidget(self.title)
        layout.addLayout(h_layout)

        self.setLayout(layout)



class SetupPage(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #006311; padding: 0px;")
        self.setFixedSize(480, 320)

        self.work_time_selector = TimerSelector('Work', 25, 1, 60)
        self.break_time_selector = TimerSelector('Break', 5, 1, 15)
        self.rest_time_selector = TimerSelector('Rest', 15, 1, 30)

        self.return_button = QPushButton()
        self.return_button.setFixedSize(44, 44)
        self.return_button.setStyleSheet("""
                    QPushButton {
                        border-radius: 22px;
                        background: rgba(0, 0, 0, 0.0)
                    }
                    QPushButton:hover {
                        background: rgba(0, 0, 0, 0.2);
                    }
                    QPushButton:pressed {
                        background: rgba(0, 0, 0, 0.1);
                    }
                """)
        self.return_button.setIcon(QIcon("./assets/return.svg"))
        self.return_button.setIconSize(QSize(32, 32))
        self.return_button.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.return_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.work_time_selector)
        layout.addWidget(self.break_time_selector)
        layout.addWidget(self.rest_time_selector)

        self.setLayout(layout)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.return_button.move(10, 10)