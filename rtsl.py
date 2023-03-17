from PyQt5.QtWidgets import QApplication

from league_database import LeagueDatabase
from application_window import ApplicationWindow


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    database = LeagueDatabase()
    window = ApplicationWindow(database)
    app.exec()
    database.close_connection()
