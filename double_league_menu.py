from typing import Optional

from PyQt5.QtWidgets import QTableWidget, QLabel, QTableWidgetItem, QWidget, QStackedWidget, QPushButton, QVBoxLayout, QComboBox, QLineEdit

from error_window import ErrorWindow
from league_menu import LeagueMenu
from match import DoubleLeagueMatch


def calculate_moved_points(diff: float, bilans: int) -> float:
    return pow((diff / 2720 + 1.7), 7.25) * (bilans / 10 + 0.5)


def calculate_ratio(player1_points: float, player2_points: float) -> float:
    return player1_points / (player1_points + player2_points)


def calculate_diff(win_player1_points: float, win_player2_points: float,
                   loose_player1_points: float, loose_player2_points: float) -> float:
    return loose_player1_points + loose_player2_points - win_player1_points - win_player2_points


class DoubleLeagueMenu(LeagueMenu):
    def __init__(self, window: QStackedWidget, database):
        super().__init__(window, database)
        self._layout = QVBoxLayout()
        self._layout.addWidget(QLabel("Double League"))
        self._add_return_button(self._window.switch_to_main_menu)
        self._players_statistics = self._add_statistics_table()
        self._add_new_match_interaction()
        self._recent_matches = self._add_recent_matches_table()
        self.update()
        self.setLayout(self._layout)

    def update(self):
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

    def _update_name_boxes(self):
        palyer_names = [''] + self._database.get_player_names()
        for name_box in self._name_boxes:
            name_box.clear()
            name_box.addItems(palyer_names)

    def _add_new_match_to_database(self, match: Optional[DoubleLeagueMatch]) -> None:
        if match is None:
            return
        self._database.insert_double_league_match(match)
        win_player1_points = self._database.get_player_dl_points(match.win_player1)
        win_player2_points = self._database.get_player_dl_points(match.win_player2)
        loose_player1_points = self._database.get_player_dl_points(match.loose_player1)
        loose_player2_points = self._database.get_player_dl_points(match.loose_player2)
        win_player2_ratio=calculate_ratio(win_player1_points, win_player2_points)
        win_player1_ratio=1-win_player2_ratio
        loose_player1_ratio=calculate_ratio(loose_player1_points, loose_player2_points)
        loose_player2_ratio=1-loose_player1_ratio
        diff=calculate_diff(win_player1_points, win_player2_points, loose_player1_points, loose_player2_points)
        points_to_add=calculate_moved_points(diff, match.goal_balance)
        self._database.update_player_dl_points(match.win_player1, win_player1_points + win_player1_ratio * points_to_add)
        self._database.update_player_dl_points(match.win_player2, win_player2_points + win_player2_ratio * points_to_add)
        self._database.update_player_dl_points(match.loose_player1, loose_player1_points - loose_player1_ratio * points_to_add)
        self._database.update_player_dl_points(match.loose_player2, loose_player2_points - loose_player2_ratio * points_to_add)
        self.update()

    def _add_recent_matches_table(self) -> QTableWidget:
        self._layout.addWidget(QLabel("Recent Matches"))
        recent_matches = QTableWidget()
        self._layout.addWidget(recent_matches)
        return recent_matches
    
    def _add_statistics_table(self) -> QTableWidget:
        self._layout.addWidget(QLabel("Statistics"))
        players_statistics = QTableWidget()
        self._layout.addWidget(players_statistics)
        return players_statistics

    def _update_player_statistcs(self) -> None:
        players = self._database.get_players()
        self._players_statistics.setColumnCount(2)
        self._players_statistics.setRowCount(len(players))
        self._players_statistics.setHorizontalHeaderLabels(('Name', 'Points'))
        for index, player in enumerate(sorted(players, key=lambda player: player.dl_points, reverse=True)):
            self._players_statistics.setItem(index, 0, QTableWidgetItem(player.name))
            self._players_statistics.setItem(index, 1, QTableWidgetItem(str(round(player.dl_points))))

    def _update_recent_matches(self) -> None:
        matches = self._database.get_double_league_matches(10)
        self._recent_matches.setColumnCount(5)
        self._recent_matches.setRowCount(len(matches))
        self._recent_matches.setHorizontalHeaderLabels(
            ('Win Player 1', 'Win Player 2', 'Loose Player 1', 'Loose Player 2', 'Goal Balance'))
        for index, match in enumerate(matches):
            self._recent_matches.setItem(index, 0, QTableWidgetItem(match.win_player1))
            self._recent_matches.setItem(index, 1, QTableWidgetItem(match.win_player2))
            self._recent_matches.setItem(index, 2, QTableWidgetItem(match.loose_player1))
            self._recent_matches.setItem(index, 3, QTableWidgetItem(match.loose_player2))
            self._recent_matches.setItem(index, 4, QTableWidgetItem(str(match.goal_balance)))
