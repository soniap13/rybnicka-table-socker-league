from typing import Callable, Optional

from PyQt5.QtWidgets import QLineEdit, QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from constants import NORMAL_TEXT_FONT, SECTION_TITLE_FONT, TITLE_FONT
from error_window import ErrorWindow
from league_database import LeagueDatabase
from utils import create_label, is_float


class PlayerDataView(QWidget):
    def __init__(self, window: QStackedWidget, database: LeagueDatabase):
        super().__init__()
        self._window = window
        self._database = database
        self._name = None
        self._layout = QVBoxLayout()
        self._layout.addWidget(create_label("Player Info", TITLE_FONT))
        self._add_return_button(self._window.switch_to_main_menu)
        self._players_statistics = self._add_statistics()
        self._recent_sl_matches = self._add_recent_sl_matches_table()
        self._recent_dl_matches = self._add_recent_dl_matches_table()
        self.setLayout(self._layout)

    def update(self, name: Optional[str] = None) -> None:
        if name is not None:
            self._name = name
        self._update_statistics()
        self._update_recent_sl_matches()
        self._update_recent_dl_matches()

    def _add_return_button(self, return_action: Callable[[], None]) -> None:
        return_button = QPushButton('Return')
        return_button.clicked.connect(return_action)
        self._layout.addWidget(return_button)
    
    def _add_statistics(self):
        name_label = create_label("Name: ", NORMAL_TEXT_FONT)
        self._name_text_box = QLineEdit()
        update_name_button = QPushButton("Update Name")
        update_name_button.clicked.connect(self._update_name_of_player)
        try_hard_factor_label = create_label("Try Hard Factor:", NORMAL_TEXT_FONT)
        self._try_hard_factor_box = QLineEdit()
        update_try_hard_factor_button = QPushButton("Update Try Hard Factor")
        update_try_hard_factor_button.clicked.connect(self._update_player_try_hard_factor)
        self._sl_points_label = create_label("", NORMAL_TEXT_FONT)
        self._dl_points_label = create_label("", NORMAL_TEXT_FONT)
        starting_dl_points_label = create_label("Starting DL points:", NORMAL_TEXT_FONT)
        self._starting_dl_points_box = QLineEdit()
        update_dl_points_button = QPushButton("Update starting DL Points")
        update_dl_points_button.clicked.connect(self._update_player_starting_dl_points)
        for label in (name_label, self._name_text_box, update_name_button, try_hard_factor_label,
                      self._try_hard_factor_box, update_try_hard_factor_button, self._sl_points_label,
                      self._dl_points_label, starting_dl_points_label, self._starting_dl_points_box,
                      update_dl_points_button):
            self._layout.addWidget(label)

    def _update_name_of_player(self) -> None:
        new_name = self._name_text_box.text()
        if self._database.is_player_in_database(new_name):
            self._error_window = ErrorWindow(f"Player {new_name} already exists in database")
            return None
        self._database.update_player_name(self._name, new_name)
        self.update(new_name)

    def _update_player_try_hard_factor(self) -> None:
        if not is_float(self._try_hard_factor_box.text()):
            self._error_window = ErrorWindow("Try Hard Factor has to be float number")
            return None
        self._database.update_player_try_hard_factor(self._name, float(self._try_hard_factor_box.text()))
        self.update()

    def _update_player_starting_dl_points(self) -> None:
        if not is_float(self._starting_dl_points_box.text()):
            self._error_window = ErrorWindow("DL points have to be float number")
            return None
        self._database.update_player_starting_dl_points(
            self._name, float(self._starting_dl_points_box.text()))
        self.update()

    def _add_recent_sl_matches_table(self) -> QTableWidget:
        self._layout.addWidget(create_label("Recent Single League Matches", SECTION_TITLE_FONT))
        recent_matches = QTableWidget()
        self._layout.addWidget(recent_matches)
        return recent_matches

    def _add_recent_dl_matches_table(self) -> QTableWidget:
        self._layout.addWidget(create_label("Recent Double League Matches", SECTION_TITLE_FONT))
        recent_matches = QTableWidget()
        self._layout.addWidget(recent_matches)
        return recent_matches
    
    def _update_statistics(self):
        self._name_text_box.setText(self._name)
        self._try_hard_factor_box.setText(str(self._database.get_player_try_hard_factor(self._name)))
        self._sl_points_label.setText(f"SL points: {self._database.get_player_sl_points(self._name)}")
        self._dl_points_label.setText(f"DL points: {self._database.get_player_dl_points(self._name)}")
        self._starting_dl_points_box.setText(str(self._database.get_player_starting_dl_points(self._name)))

    def _update_recent_dl_matches(self) -> None:
        matches = self._database.get_player_recent_double_league_matches(self._name, 5)
        self._recent_dl_matches.setColumnCount(5)
        self._recent_dl_matches.setRowCount(len(matches))
        self._recent_dl_matches.setHorizontalHeaderLabels(
            ('Winning Player 1', 'Winning Player 2', 'Loser Player 1', 'Loser Player 2', 'Goal Balance'))
        for index, match in enumerate(matches):
            self._recent_dl_matches.setItem(index, 0, QTableWidgetItem(match.winning_player1))
            self._recent_dl_matches.setItem(index, 1, QTableWidgetItem(match.winning_player2))
            self._recent_dl_matches.setItem(index, 2, QTableWidgetItem(match.loser_player1))
            self._recent_dl_matches.setItem(index, 3, QTableWidgetItem(match.loser_player2))
            self._recent_dl_matches.setItem(index, 4, QTableWidgetItem(str(match.goal_balance)))

    def _update_recent_sl_matches(self) -> None:
        matches = self._database.get_player_single_league_matches(self._name, 5)
        self._recent_sl_matches.setColumnCount(3)
        self._recent_sl_matches.setRowCount(len(matches))
        self._recent_sl_matches.setHorizontalHeaderLabels(('Winning Player', 'Loser Player', 'Goal Balance'))
        for index, match in enumerate(matches):
            self._recent_sl_matches.setItem(index, 0, QTableWidgetItem(match.winning_player))
            self._recent_sl_matches.setItem(index, 1, QTableWidgetItem(match.loser_player))
            self._recent_sl_matches.setItem(index, 2, QTableWidgetItem(str(match.goal_balance)))
