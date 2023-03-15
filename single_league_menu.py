from PyQt5.QtWidgets import QWidget, QStackedWidget, QPushButton, QVBoxLayout, QComboBox, QLabel, QLineEdit

from widget import Widget


class SingleLeagueMenu(Widget):
    def __init__(self, window, database):
        super().__init__(window, database)
        self._layout = QVBoxLayout()
        self._layout.addWidget(QLabel("Single League"))
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
        score_box = QLineEdit()
        self._layout.addWidget(name1_box)
        self._layout.addWidget(name2_box)
        self._layout.addWidget(score_box)
        add_button = QPushButton('Add')
        add_button.clicked.connect(lambda: self._add_new_match_to_database(
            name1_box.currentText(), name2_box.currentText(), int(score_box.text())))
        self._layout.addWidget(add_button)

    def _add_new_match_to_database(self, win_player: str, loose_player: str, goal_balance: int) -> None:
        self._database.insert_single_league_match(win_player, loose_player, goal_balance)
        print(self._database.get_single_league_matches())
        self._database.update_player_points(win_player, self._database.get_player_points(win_player) + goal_balance)
        self._database.update_player_points(loose_player, self._database.get_player_points(loose_player) - goal_balance)