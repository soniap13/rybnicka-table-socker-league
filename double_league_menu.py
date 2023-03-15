from PyQt5.QtWidgets import QLabel, QWidget, QStackedWidget, QPushButton, QVBoxLayout, QComboBox, QLineEdit

from widget import Widget


def calculate_moved_points(diff: float, bilans: int) -> float:
    return pow((diff / 2720 + 1.7), 7.25) * (bilans / 10 + 0.5)


def calculate_ratio(player1_points: float, player2_points: float) -> float:
    return player1_points / (player1_points + player2_points)


def calculate_diff(win_player1_points: float, win_player2_points: float,
                   loose_player1_points: float, loose_player2_points: float) -> float:
    return loose_player1_points + loose_player2_points - win_player1_points - win_player2_points


class DoubleLeagueMenu(Widget):
    def __init__(self, window: QStackedWidget, database):
        super().__init__(window, database)
        self._layout = QVBoxLayout()
        self._layout.addWidget(QLabel("Double League"))
        self._add_return_button(self._window.switch_to_main_menu)
        self._add_player_data_interaction()
        self._add_new_match_interaction()
        self._display_players_statistics()
        self.setLayout(self._layout)

    def _add_new_match_interaction(self) -> None:
        self._layout.addWidget(QLabel("Add new match"))
        name1_box = QComboBox()
        name1_box.addItems(self._database.get_player_names())
        name2_box = QComboBox()
        name2_box.addItems(self._database.get_player_names())
        name3_box = QComboBox()
        name3_box.addItems(self._database.get_player_names())
        name4_box = QComboBox()
        name4_box.addItems(self._database.get_player_names())
        score_box = QLineEdit()
        self._layout.addWidget(name1_box)
        self._layout.addWidget(name2_box)
        self._layout.addWidget(name3_box)
        self._layout.addWidget(name4_box)
        self._layout.addWidget(score_box)
        add_button = QPushButton('Add')
        add_button.clicked.connect(lambda: self._add_new_match_to_database(
            name1_box.currentText(), name2_box.currentText(),
            name3_box.currentText(), name4_box.currentText(), int(score_box.text())))
        self._layout.addWidget(add_button)
 


    def _add_new_match_to_database(self, win_player1: str, win_player2: str, loose_player1: str, loose_player2: str, goal_balance: int) -> None:
        self._database.insert_double_league_match(win_player1, win_player2, loose_player1, loose_player1, goal_balance)
        win_player1_points = self._database.get_player_points(win_player1)
        win_player2_points = self._database.get_player_points(win_player2)
        loose_player1_points = self._database.get_player_points(loose_player1)
        loose_player2_points = self._database.get_player_points(loose_player2)
        win_player2_ratio=calculate_ratio(win_player1_points, win_player2_points)
        win_player1_ratio=1-win_player2_ratio
        loose_player1_ratio=calculate_ratio(loose_player1_points, loose_player2_points)
        loose_player2_ratio=1-loose_player1_ratio
        diff=calculate_diff(win_player1_points, win_player2_points, loose_player1_points, loose_player2_points)
        points_to_add=calculate_moved_points(diff, goal_balance)
        self._database.update_player_points(win_player1, win_player1_points + win_player1_ratio * points_to_add)
        self._database.update_player_points(win_player2, win_player2_points + win_player2_ratio * points_to_add)
        self._database.update_player_points(loose_player1, loose_player1_points - loose_player1_ratio * points_to_add)
        self._database.update_player_points(loose_player2, loose_player2_points - loose_player2_ratio * points_to_add)
