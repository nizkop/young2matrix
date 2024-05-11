from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor

def colorize_pixmap(icon:QIcon, color:str) -> QPixmap:
    """ method needed for a changeable color of an icon in a button """
    # print("colorize pixmap:", color, flush=True)
    pixmap = icon.pixmap(32, 32)
    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(Qt.transparent)
    painter = QPainter(colored_pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.drawPixmap(pixmap.rect(), pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(colored_pixmap.rect(), color)
    painter.end()
    return colored_pixmap

def get_colored_icon_button(button:QPushButton, file_path:str, color:str) -> QPushButton:
    """ setting up a button build from an icon (instead of text as usual)
    and triggering the coloring
    """
    # print("get_colored_icon_button", color, flush=True)
    icon = QIcon(file_path)
    colored_pixmap = colorize_pixmap(icon=icon, color=QColor(color))
    button.setIcon(QIcon(colored_pixmap))
    return button
