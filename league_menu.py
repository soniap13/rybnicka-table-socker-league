from typing import Callable

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QLabel, QStackedWidget, QPushButton, QVBoxLayout, QLineEdit, QListWidget

from league_database import LeagueDatabase


class LeagueMenu(QWidget):
    def __init__(self, window: QStackedWidget, database: LeagueDatabase):
        super().__init__()
        self._window = window
        self._database = database

    def _add_return_button(self, return_action: Callable[[], None]) -> None:
        return_button = QPushButton('Return')
        return_button.clicked.connect(return_action)
        self._layout.addWidget(return_button)
