from PyQt5.QtWidgets import QLabel, QWidget, QStackedWidget, QPushButton, QVBoxLayout, QComboBox, QLineEdit

from widget import Widget


class DoubleLeagueMenu(Widget):
    def __init__(self, window: QStackedWidget):
        super().__init__(window)
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
        name2_box = QComboBox()
        name3_box = QComboBox()
        name4_box = QComboBox()
        score_box = QLineEdit()
        self._layout.addWidget(name1_box)
        self._layout.addWidget(name2_box)
        self._layout.addWidget(name3_box)
        self._layout.addWidget(name4_box)
        self._layout.addWidget(score_box)
        add_button = QPushButton('Add')
        self._layout.addWidget(add_button)
