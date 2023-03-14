from PyQt5.QtWidgets import QApplication

from main_menu import Window


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = Window()
    app.exec()
