from typing import Callable

from PyQt5.QtWidgets import QWidget, QLabel, QStackedWidget, QPushButton, QVBoxLayout, QLineEdit


class Widget(QWidget):
    def __init__(self, window: QStackedWidget):
        super().__init__()
        self._window = window

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

    def _add_new_player_to_database(self, name: str) -> None:
        print(f"adding new player {name}")
