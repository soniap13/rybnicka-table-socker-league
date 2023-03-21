from typing import Optional

from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTableWidgetItem

from error_window import ErrorWindow
from league_menu import LeagueMenu
from match import SingleLeagueMatch


class SingleLeagueMenu(LeagueMenu):
    def __init__(self, window, database):
        super().__init__(window, database)
        self._layout = QVBoxLayout()
        self._layout.addWidget(QLabel("Single League"))
        self._add_return_button(self._window.switch_to_main_menu)
        self._players_statistics = self._add_statistics_table()
        self._add_new_match_interaction()
        self._recent_matches = self._add_recent_matches_table()
        self.setLayout(self._layout)

    def update(self) -> None:
        self._update_player_statistcs()
        self._update_recent_matches()
        self._update_name_boxes()

    def _add_new_match_interaction(self) -> None:
        self._layout.addWidget(QLabel("Add new match"))
        self._name1_box = QComboBox()
        self._name2_box = QComboBox()
        self._score_box = QLineEdit()
        self._layout.addWidget(self._name1_box)
        self._layout.addWidget(self._name2_box)
        self._layout.addWidget(self._score_box)
        add_button = QPushButton('Add')
        add_button.clicked.connect(lambda: self._add_new_match_to_database(
            self._get_validated_match()))
        self._layout.addWidget(add_button)

    def _get_validated_match(self) -> Optional[SingleLeagueMatch]:
        player_names = (self._name1_box.currentText(), self._name2_box.currentText())
        if any([player_name == '' for player_name in player_names]):
            self._error_window = ErrorWindow("Name of one of the players was left empty")
            return None
        if len(set(player_names)) != len(player_names):
            self._error_window = ErrorWindow("Names of the players can't be repeated")
            return None
        goal_balance = self._score_box.text()
        if goal_balance not in (str(i) for i in range(11)):
            self._error_window = ErrorWindow("Goal balnce must be an integer between 0 and 10")
            return None
        self._score_box.clear()
        return SingleLeagueMatch(*player_names, int(goal_balance))

    def _update_name_boxes(self) -> None:
        player_names = [''] + self._database.get_player_names()
        for name_box in (self._name1_box, self._name2_box):
            name_box.clear()
            name_box.addItems(player_names)

    def _add_new_match_to_database(self, match: Optional[SingleLeagueMatch]) -> None:
        if match is not None:
            self._database.insert_single_league_match(match)
            self.update()

    def _update_player_statistcs(self) -> None:
        players = self._database.get_player_names()
        self._players_statistics.setColumnCount(2)
        self._players_statistics.setRowCount(len(players))
        self._players_statistics.setHorizontalHeaderLabels(('Name', 'Points'))
        for index, player in enumerate(
                sorted(players, key=lambda player: self._database.get_player_sl_points(player),
                       reverse=True)):
            self._players_statistics.setItem(index, 0, QTableWidgetItem(player))
            self._players_statistics.setItem(index, 1, QTableWidgetItem(
                str(self._database.get_player_sl_points(player))))

    def _update_recent_matches(self) -> None:
        matches = self._database.get_single_league_matches(10)
        self._recent_matches.setColumnCount(3)
        self._recent_matches.setRowCount(len(matches))
        self._recent_matches.setHorizontalHeaderLabels(('Winning Player', 'Loser Player', 'Goal Balance'))
        for index, match in enumerate(matches):
            self._recent_matches.setItem(index, 0, QTableWidgetItem(match.winning_player))
            self._recent_matches.setItem(index, 1, QTableWidgetItem(match.loser_player))
            self._recent_matches.setItem(index, 2, QTableWidgetItem(str(match.goal_balance)))
