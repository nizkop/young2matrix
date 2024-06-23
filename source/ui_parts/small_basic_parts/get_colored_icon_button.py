from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor

from source.settings.GLOBALS import FILE_PATH_SETTINGS_ICON


def colorize_pixmap(icon:QIcon, color:str) -> QPixmap:
    """ method needed for a changeable color of an icon in a button
     :param icon: ui icon, that shall be changed
     :param color: color, the icon should be changed into
     :return: colored icon object
    """
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

def get_colored_icon_button(button:QPushButton, color:str) -> QPushButton:
    """ setting up a button build from an icon (instead of text as usual)
    and triggering the coloring
    :param button: ui button, that needs to be customized
    :param color: color the button icon should have
    :return: colored button
    """
    icon = QIcon(FILE_PATH_SETTINGS_ICON)
    if "rgb" in color:
        color = color.replace("rgb","").replace("(","").replace(")","")
        r, g, b = color.split(',')
        colored_pixmap = colorize_pixmap(icon=icon,color=QColor(int(r),int(g),int(b)))
    else:
        colored_pixmap = colorize_pixmap(icon=icon, color=QColor(color))
    button.setIcon(QIcon(colored_pixmap))
    return button

