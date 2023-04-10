from typing import Callable

from PyQt5.QtWidgets import QPushButton, QStackedWidget, QTableWidget, QWidget

from constants import SECTION_TITLE_FONT
from league_database import LeagueDatabase
from utils import create_label


class LeagueMenu(QWidget):
    def __init__(self, window: QStackedWidget, database: LeagueDatabase):
        super().__init__()
        self._window = window
        self._database = database

    def _add_return_button(self, return_action: Callable[[], None]) -> None:
        return_button = QPushButton('Return')
        return_button.clicked.connect(return_action)
        self._layout.addWidget(return_button)

    def _add_recent_matches_table(self) -> QTableWidget:
        self._layout.addWidget(create_label("Recent Matches", SECTION_TITLE_FONT))
        recent_matches = QTableWidget()
        self._layout.addWidget(recent_matches)
        return recent_matches

    def _add_player_statistics_table(self) -> QTableWidget:
        self._layout.addWidget(create_label("Players Statistics", SECTION_TITLE_FONT))
        players_statistics = QTableWidget()
        self._layout.addWidget(players_statistics)
        return players_statistics
