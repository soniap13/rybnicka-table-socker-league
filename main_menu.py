from copy import copy
from dataclasses import dataclass
from typing import Optional
from functools import partial

from PyQt5.QtWidgets import (
    QCheckBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from constants import SECTION_TITLE_FONT
from error_window import ErrorWindow
from league_database import LeagueDatabase
from utils import create_label, is_float


@dataclass
class PlayerStartingData:
    name: str
    dl_points: float
    try_hard_factor: float


class MainMenu(QWidget):
    def __init__(self, window, database: LeagueDatabase):
        super().__init__()
        self._window = window
        self._database = database
        self._layout = QVBoxLayout()
        self._add_single_league_button()
        self._add_double_league_button()
        self._add_player_data_interaction()
        self._add_players_statistics_table()
        self.setLayout(self._layout)
    
    def update(self) -> None:
        self._update_player_statistics()

    def _add_single_league_button(self) -> None:
        single_league_button = QPushButton('Single League')
        single_league_button.clicked.connect(self._window.switch_to_single_league_menu)
        self._layout.addWidget(single_league_button)

    def _add_double_league_button(self) -> None:
        double_league_button = QPushButton('Double League')
        double_league_button.clicked.connect(self._window.switch_to_double_league_menu)
        self._layout.addWidget(double_league_button)

    def _add_player_data_interaction(self) -> None:
        self._layout.addWidget(create_label("Add new player", SECTION_TITLE_FONT))
        self._layout.addWidget(create_label("Name:"))
        self._name_box = QLineEdit()
        self._layout.addWidget(self._name_box)
        self._layout.addWidget(create_label("Starting points for Double League:"))
        self._starting_points_box = QLineEdit()
        self._layout.addWidget(self._starting_points_box)
        self._try_hard_check_box = QCheckBox()
        self._try_hard_check_box.setText("Try Hard")
        self._layout.addWidget(self._try_hard_check_box)
        add_button = QPushButton('Add')
        add_button.clicked.connect(
            lambda: self._add_new_player_to_database(self._get_validated_player()))
        self._layout.addWidget(add_button)
    
    def _get_validated_player(self) -> Optional[PlayerStartingData]:
        player_name = self._name_box.text()
        starting_points = self._starting_points_box.text()
        if player_name == '':
            self._error_window = ErrorWindow("Name od the player must be specified")
            return None
        if not is_float(starting_points):
            self._error_window = ErrorWindow("Starting points for double league must be specified")
            return None
        self._name_box.clear()
        self._starting_points_box.clear()
        try_hard_factor = 1 if bool(self._try_hard_check_box.isChecked()) else 0
        self._try_hard_check_box.setChecked(False)
        return PlayerStartingData(player_name, float(starting_points), try_hard_factor)

    def _add_players_statistics_table(self) -> None:
        self._layout.addWidget(create_label("Statisctics", SECTION_TITLE_FONT))
        self._players_statistics = QTableWidget()
        self._players_statistics.setHorizontalHeaderLabels(('Name', 'SL Points', 'DL Points'))
        self._layout.addWidget(self._players_statistics)

    def _update_player_statistics(self) -> None:
        players = self._database.get_player_names()
        self._players_statistics.setColumnCount(3)
        self._players_statistics.setRowCount(len(players))
        #self._players_statistics.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._players_statistics.setHorizontalHeaderLabels(("Player", "SL score", "DL core"))
        for index, player in enumerate(players):
            self._players_statistics.setCellWidget(index, 0, QPushButton(player))
            self._players_statistics.cellWidget(index, 0).clicked.connect(
                partial(self._window.switch_to_player_data_view, player))
            self._players_statistics.setItem(index, 1, QTableWidgetItem(
                str(self._database.get_player_sl_points(player))))
            self._players_statistics.setItem(index, 2, QTableWidgetItem(
                str(self._database.get_player_dl_points(player))))

    def _add_new_player_to_database(self, player: Optional[PlayerStartingData]) -> None:
        if player is not None:
            if player.name in self._database.get_player_names():
                self._error_window(f"Player {player.name} already exists in database")
            self._database.insert_player(player)
            self._update_player_statistics()
