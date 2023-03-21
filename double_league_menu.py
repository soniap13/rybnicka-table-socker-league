from typing import Optional

from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

from error_window import ErrorWindow
from league_menu import LeagueMenu
from match import DoubleLeagueMatch


def calculate_moved_points(diff: float, bilans: int) -> float:
    return pow((diff / 2720 + 1.7), 7.25) * (bilans / 10 + 0.5)


def calculate_ratio(player1_points: float, player2_points: float) -> float:
    return player1_points / (player1_points + player2_points)


def calculate_diff(winning_player1_points: float, winning_player2_points: float,
                   loser_player1_points: float, loser_player2_points: float) -> float:
    return loser_player1_points + loser_player2_points - winning_player1_points - winning_player2_points


class DoubleLeagueMenu(LeagueMenu):
    def __init__(self, window, database):
        super().__init__(window, database)
        self._layout = QVBoxLayout()
        self._layout.addWidget(QLabel("Double League"))
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
        if goal_balance not in (str(i) for i in range(11)):
            self._error_window = ErrorWindow("Goal balnce must be an integer between 0 and 10")
            return None
        self._score_box.clear()
        return DoubleLeagueMatch(*player_names, int(goal_balance))

    def _update_name_boxes(self) -> None:
        palyer_names = [''] + self._database.get_player_names()
        for name_box in self._name_boxes:
            name_box.clear()
            name_box.addItems(palyer_names)

    def _add_new_match_to_database(self, match: Optional[DoubleLeagueMatch]) -> None:
        if match is None:
            return
        self._database.insert_double_league_match(match)
        winning_player1_points = self._database.get_player_dl_points(match.winning_player1)
        winning_player2_points = self._database.get_player_dl_points(match.winning_player2)
        loser_player1_points = self._database.get_player_dl_points(match.loser_player1)
        loser_player2_points = self._database.get_player_dl_points(match.loser_player2)
        winning_player2_ratio=calculate_ratio(winning_player1_points, winning_player2_points)
        winning_player1_ratio=1-winning_player2_ratio
        loser_player1_ratio=calculate_ratio(loser_player1_points, loser_player2_points)
        loser_player2_ratio=1-loser_player1_ratio
        diff=calculate_diff(winning_player1_points, winning_player2_points, loser_player1_points, loser_player2_points)
        points_to_add=calculate_moved_points(diff, match.goal_balance)
        self._database.update_player_dl_points(match.winning_player1, winning_player1_points + winning_player1_ratio * points_to_add)
        self._database.update_player_dl_points(match.winning_player2, winning_player2_points + winning_player2_ratio * points_to_add)
        self._database.update_player_dl_points(match.loser_player1, loser_player1_points - loser_player1_ratio * points_to_add)
        self._database.update_player_dl_points(match.loser_player2, loser_player2_points - loser_player2_ratio * points_to_add)
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

    def _update_recent_matches(self) -> None:
        matches = self._database.get_double_league_matches(10)
        self._recent_matches.setColumnCount(5)
        self._recent_matches.setRowCount(len(matches))
        self._recent_matches.setHorizontalHeaderLabels(
            ('Winning Player 1', 'Winning Player 2', 'Loser Player 1', 'Loser Player 2', 'Goal Balance'))
        for index, match in enumerate(matches):
            self._recent_matches.setItem(index, 0, QTableWidgetItem(match.winning_player1))
            self._recent_matches.setItem(index, 1, QTableWidgetItem(match.winning_player2))
            self._recent_matches.setItem(index, 2, QTableWidgetItem(match.loser_player1))
            self._recent_matches.setItem(index, 3, QTableWidgetItem(match.loser_player2))
            self._recent_matches.setItem(index, 4, QTableWidgetItem(str(match.goal_balance)))
