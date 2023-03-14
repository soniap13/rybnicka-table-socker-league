from PyQt5.QtWidgets import QWidget, QStackedWidget, QPushButton, QVBoxLayout

from double_league_menu import DoubleLeagueMenu
from single_league_menu import SingleLeagueMenu
from widget import Widget


class MainMenu(Widget):
     def __init__(self, window: QStackedWidget):
        super().__init__(window)
        self._window = window
        self._layout = QVBoxLayout()
        single_league_button = QPushButton('Single League')
        single_league_button.clicked.connect(self._window.switch_to_single_league_menu)
        self._layout.addWidget(single_league_button)
        double_league_button = QPushButton('Double League')
        double_league_button.clicked.connect(self._window.switch_to_double_league_menu)
        self._layout.addWidget(double_league_button)
        self.setLayout(self._layout)

class Window(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RTSL (Rybnicka Table Soccer League)'")
        self._main_menu = MainMenu(self)
        self.addWidget(self._main_menu)
        self._single_league_menu = SingleLeagueMenu(self)
        self.addWidget(self._single_league_menu)
        self._double_league_menu = DoubleLeagueMenu(self)
        self.addWidget(self._double_league_menu)
        self.setCurrentWidget(self._main_menu)
        self.show()

    def switch_to_single_league_menu(self) -> None:
        self.setCurrentWidget(self._single_league_menu)

    def switch_to_double_league_menu(self) -> None:
        self.setCurrentWidget(self._double_league_menu)

    def switch_to_main_menu(self) -> None:
        self.setCurrentWidget(self._main_menu)
