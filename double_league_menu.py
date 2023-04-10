from functools import partial
from itertools import combinations
from typing import Optional

from PyQt5.QtWidgets import QComboBox, QLineEdit, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

from constants import POSSIBLE_GOAL_BALANCES, SECTION_TITLE_FONT, TITLE_FONT
from error_window import ErrorWindow
from league_menu import LeagueMenu
from match import DoubleLeagueMatch
from utils import create_label


class DoubleLeagueMenu(LeagueMenu):
    def __init__(self, window, database):
        super().__init__(window, database)
        self._layout = QVBoxLayout()
        self._layout.addWidget(create_label("Double League", TITLE_FONT))
        self._add_return_button(self._window.switch_to_main_menu)
        self._players_statistics = self._add_player_statistics_table()
        self._teams_statistics = self._add_teams_statistics_table()
        self._add_new_match_interaction()
        self._recent_matches = self._add_recent_matches_table()
        self.setLayout(self._layout)

    def update(self) -> None:
        self._update_player_statistcs()
        self._update_teams_statistics()
        self._update_recent_matches()
        self._update_name_boxes()

    def _add_new_match_interaction(self) -> None:
        self._layout.addWidget(create_label("Add new match", SECTION_TITLE_FONT))
        self._name_boxes = [QComboBox() for _ in range(4)]
        self._score_box = QLineEdit()
        for name_box in self._name_boxes:
            self._layout.addWidget(name_box)
        self._layout.addWidget(self._score_box)
        add_button = QPushButton('Add')
        add_button.clicked.connect(lambda: self._add_new_match_to_database(
            self._get_validated_match()))
        self._layout.addWidget(add_button)

    def _get_validated_match(self) -> Optional[DoubleLeagueMatch]:
        player_names = [name_box.currentText() for name_box in self._name_boxes]
        if any([player_name == '' for player_name in player_names]):
            self._error_window = ErrorWindow("Name of one of the players was left empty")
            return None
        if len(set(player_names)) != len(player_names):
            self._error_window = ErrorWindow("Names of the players can't be repeated")
            return None
        goal_balance = self._score_box.text()
        if goal_balance not in POSSIBLE_GOAL_BALANCES:
            self._error_window = ErrorWindow("Goal balnce must be an integer between 0 and 10")
            return None
        self._score_box.clear()
        return DoubleLeagueMatch(None, *player_names, int(goal_balance))

    def _update_name_boxes(self) -> None:
        palyer_names = [''] + self._database.get_player_names()
        for name_box in self._name_boxes:
            name_box.clear()
            name_box.addItems(palyer_names)

    def _add_new_match_to_database(self, match: Optional[DoubleLeagueMatch]) -> None:
        if match is None:
            return
        self._database.insert_double_league_match(match)
        self.update()

    def _update_player_statistcs(self) -> None:
        players = self._database.get_player_names()
        self._players_statistics.setColumnCount(2)
        self._players_statistics.setRowCount(len(players))
        self._players_statistics.setHorizontalHeaderLabels(('Name', 'Points'))
        for index, player in enumerate(
                sorted(players, key=lambda player: self._database.get_player_dl_points(player), reverse=True)):
            self._players_statistics.setItem(index, 0, QTableWidgetItem(player))
            self._players_statistics.setItem(index, 1, QTableWidgetItem(
                str(self._database.get_player_dl_points(player))))

    def _update_teams_statistics(self) -> None:
        players = self._database.get_player_names()
        teams = combinations(players, 2)
        self._teams_statistics.setColumnCount(3)
        self._teams_statistics.setRowCount(len(players))
        self._teams_statistics.setHorizontalHeaderLabels(('Player1', 'Player2', 'Points'))
        teams_dl_points = {team: self._database.get_team_dl_points(*team) for team in teams}
        for index, ((player1, player2), dl_points) in enumerate(
                sorted(teams_dl_points.items(), key=lambda record: record[1])):
            self._teams_statistics.setItem(index, 0, QTableWidgetItem(player1))
            self._teams_statistics.setItem(index, 1, QTableWidgetItem(player2))
            self._teams_statistics.setItem(index, 2, QTableWidgetItem(str(dl_points)))

    def _update_recent_matches(self) -> None:
        matches = self._database.get_double_league_matches(10)
        self._recent_matches.setColumnCount(6)
        self._recent_matches.setRowCount(len(matches))
        self._recent_matches.setHorizontalHeaderLabels(
            ('Winning Player 1', 'Winning Player 2', 'Loser Player 1', 'Loser Player 2', 'Goal Balance', ''))
        for index, match in enumerate(matches):
            self._recent_matches.setItem(index, 0, QTableWidgetItem(match.winning_player1))
            self._recent_matches.setItem(index, 1, QTableWidgetItem(match.winning_player2))
            self._recent_matches.setItem(index, 2, QTableWidgetItem(match.loser_player1))
            self._recent_matches.setItem(index, 3, QTableWidgetItem(match.loser_player2))
            self._recent_matches.setItem(index, 4, QTableWidgetItem(str(match.goal_balance)))
            self._recent_matches.setCellWidget(index, 5, QPushButton("Delete"))
            self._recent_matches.cellWidget(index, 5).clicked.connect(
                partial(self._delete_match, match.id))

    def _delete_match(self, match_id: int) -> None:
        self._database.delete_dl_match(match_id)
        self.update()

    def _add_teams_statistics_table(self) -> QTableWidget:
        self._layout.addWidget(create_label("Teams Statistics", SECTION_TITLE_FONT))
        teams_statistics = QTableWidget()
        self._layout.addWidget(teams_statistics)
        return teams_statistics
