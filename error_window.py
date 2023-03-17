from pyQt4 import QLabel, QVBoxLayout, QWidget

class ErrorWindow(QWidget):
    def __init__(self):
        self._layout = QVBoxLayout()
        self._layout.addWidget(QLabel("Error"))
        self.setLayout(self._layout)
