from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

from utils import create_label


class ErrorWindow(QWidget):
    def __init__(self, error_message: str):
        super().__init__()
        self._layout = QVBoxLayout()
        self._layout.addWidget(create_label(error_message))
        self.setLayout(self._layout)
        ok_button = QPushButton()
        ok_button.setText('OK')
        ok_button.clicked.connect(lambda: self.close())
        self._layout.addWidget(ok_button)
        self.show()
