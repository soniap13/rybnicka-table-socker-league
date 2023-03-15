from PyQt5.QtWidgets import QApplication

from database import Database
from main_menu import Window


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    database = Database()
    window = Window(database)
    app.exec()
    database.close_connection()
