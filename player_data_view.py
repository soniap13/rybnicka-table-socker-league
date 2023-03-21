from typing import Callable

from PyQt5.QtWidgets import QLabel, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from league_database import LeagueDatabase


class PlayerDataView(QWidget):
    def __init__(self, window: QStackedWidget, database: LeagueDatabase):
        super().__init__()
        self._window = window
        self._database = database
        self._name = None
        self._layout = QVBoxLayout()
        self._layout.addWidget(QLabel("Single League"))
        self._add_return_button(self._window.switch_to_main_menu)
        self.setLayout(self._layout)

    def update():
        pass

    def _add_return_button(self, return_action: Callable[[], None]) -> None:
        return_button = QPushButton('Return')
        return_button.clicked.connect(return_action)
        self._layout.addWidget(return_button)
