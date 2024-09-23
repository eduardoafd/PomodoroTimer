from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

app = QApplication([])

window = QWidget()
button = QPushButton('Click Me')

# Set a custom property `customState` to have multiple values
button.setProperty('customState', 'state1')

# Apply the stylesheet based on the custom property
button.setStyleSheet("""
    QPushButton[customState="state1"] {
        background-color: #4CAF50;
        color: white;
    }

    QPushButton[customState="state2"] {
        background-color: #FF5733;
        color: white;
    }

    QPushButton[customState="state3"] {
        background-color: #2196F3;
        color: white;
    }
""")


# Function to cycle between three states
def toggle_custom_state():
    current_state = button.property('customState')

    if current_state == 'state1':
        button.setProperty('customState', 'state2')
    elif current_state == 'state2':
        button.setProperty('customState', 'state3')
    else:
        button.setProperty('customState', 'state1')

    # Reapply the stylesheet to update the visual state
    button.style().unpolish(button)
    button.style().polish(button)


button.clicked.connect(toggle_custom_state)

layout = QVBoxLayout()
layout.addWidget(button)
window.setLayout(layout)
window.show()

app.exec_()
