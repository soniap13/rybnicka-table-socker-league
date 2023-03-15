from typing import Callable

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QLabel, QStackedWidget, QPushButton, QVBoxLayout, QLineEdit, QListWidget

from database import Database


class Widget(QWidget):
    def __init__(self, window: QStackedWidget, database: Database):
        super().__init__()
        self._window = window
        self._database = database

    def _add_return_button(self, return_action: Callable[[], None]) -> None:
        return_button = QPushButton('Return')
        return_button.clicked.connect(return_action)
        self._layout.addWidget(return_button)

    def _add_player_data_interaction(self) -> None:
        self._layout.addWidget(QLabel("Add new player"))
        name_box = QLineEdit()
        self._layout.addWidget(name_box)
        add_button = QPushButton('Add')
        add_button.clicked.connect(lambda: self._add_new_player_to_database(name_box.text()))
        self._layout.addWidget(add_button)
    
    def _display_players_statistics(self) -> None:
        self._layout.addWidget(QLabel("Players statistics"))
        players = self._database.get_players()
        players_statistic = QTableWidget()
        players_statistic.setColumnCount(2)
        players_statistic.setRowCount(len(players))
        players_statistic.setHorizontalHeaderLabels(('Name', 'Points'))
        for index, (name, points) in enumerate(players):
            players_statistic.setItem(index, 0, QTableWidgetItem(name))
            players_statistic.setItem(index, 1, QTableWidgetItem(points))
        self._layout.addWidget(players_statistic)

    def _add_new_player_to_database(self, name: str) -> None:
        self._database.insert_player(name, 0)
        print(self._database.get_players())
