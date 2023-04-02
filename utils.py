from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont

from constants import NORMAL_TEXT_FONT


def is_float(text: str) -> bool:
    return text.replace('.', '', 1).isnumeric()


def create_label(text: str, font: QFont = NORMAL_TEXT_FONT) -> QLabel:
    label = QLabel(text)
    label.setFont(font)
    return label
