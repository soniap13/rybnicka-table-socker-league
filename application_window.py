from PyQt5.QtWidgets import QStackedWidget

from double_league_menu import DoubleLeagueMenu
from main_menu import MainMenu
from league_database import LeagueDatabase
from player_data_view import PlayerDataView
from single_league_menu import SingleLeagueMenu


class ApplicationWindow(QStackedWidget):
    def __init__(self, database: LeagueDatabase):
        super().__init__()
        self.setWindowTitle("RTSL (Rybnicka Table Soccer League)")
        self._main_menu = MainMenu(self, database)
        self.addWidget(self._main_menu)
        self._single_league_menu = SingleLeagueMenu(self, database)
        self.addWidget(self._single_league_menu)
        self._double_league_menu = DoubleLeagueMenu(self, database)
        self.addWidget(self._double_league_menu)
        self._player_data_view = PlayerDataView(self, database)
        self.addWidget(self._player_data_view)
        self.setCurrentWidget(self._main_menu)
        self.show()

    def switch_to_single_league_menu(self) -> None:
        self._single_league_menu.update()
        self.setCurrentWidget(self._single_league_menu)

    def switch_to_double_league_menu(self) -> None:
        self._double_league_menu.update()
        self.setCurrentWidget(self._double_league_menu)

    def switch_to_main_menu(self) -> None:
        self._main_menu.update()
        self.setCurrentWidget(self._main_menu)

    def switch_to_player_data_view(self, name: str) -> None:
        self._player_data_view.update(name)
        self.setCurrentWidget(self._player_data_view)
