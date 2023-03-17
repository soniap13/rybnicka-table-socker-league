from PyQt5.QtWidgets import QWidget, QCheckBox, QTableWidget, QTableWidgetItem, QStackedWidget, QPushButton, QVBoxLayout, QComboBox, QLabel, QLineEdit

from league_database import LeagueDatabase


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
    
    def _add_single_league_button(self) -> None:
        single_league_button = QPushButton('Single League')
        single_league_button.clicked.connect(self._window.switch_to_single_league_menu)
        self._layout.addWidget(single_league_button)

    def _add_double_league_button(self) -> None:
        double_league_button = QPushButton('Double League')
        double_league_button.clicked.connect(self._window.switch_to_double_league_menu)
        self._layout.addWidget(double_league_button)

    def _add_player_data_interaction(self) -> None:
        self._layout.addWidget(QLabel("Add new player"))
        self._layout.addWidget(QLabel("Name:"))
        name_box = QLineEdit()
        self._layout.addWidget(name_box)
        self._layout.addWidget(QLabel("Starting points for Double League:"))
        starting_points_box = QLineEdit()
        self._layout.addWidget(starting_points_box)
        try_hard_check_box = QCheckBox()
        try_hard_check_box.setText("Try Hard")
        self._layout.addWidget(try_hard_check_box)
        add_button = QPushButton('Add')
        add_button.clicked.connect(
            lambda: self._add_new_player_to_database(
                name_box.text(), float(starting_points_box.text()), try_hard_check_box.isChecked()))
        self._layout.addWidget(add_button)
    
    def _add_players_statistics_table(self) -> None:
        self._layout.addWidget(QLabel("Statisctics"))
        self._players_statistics = QTableWidget()
        self._players_statistics.setHorizontalHeaderLabels(('Name', 'SL Points', 'DL Points'))
        self._update_player_statistics()
        self._layout.addWidget(self._players_statistics)

    def _update_player_statistics(self) -> None:
        players = self._database.get_players()
        self._players_statistics.setColumnCount(3)
        self._players_statistics.setRowCount(len(players))
        for index, player in enumerate(players):
            self._players_statistics.setItem(index, 0, QTableWidgetItem(player.name))
            self._players_statistics.setItem(index, 1, QTableWidgetItem(str(player.sl_points)))
            self._players_statistics.setItem(index, 2, QTableWidgetItem(str(player.dl_points)))

    def _add_new_player_to_database(self, name: str, starting_points: float, is_try_hard: bool) -> None:
        self._database.insert_player(name, starting_points, is_try_hard)
        self._update_player_statistics()
