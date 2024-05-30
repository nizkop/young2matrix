from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part


def get_basic_label(content:str, allowed_width):
    """

    :param content: e.g. html formatted text
    :return: ui label, that can be added to a layout
    """
    label = QLabel(content)
    label.setWordWrap(True)#ensure line break...
    label.setMaximumWidth(allowed_width)#...at fixed width
    label.setTextFormat(Qt.RichText)#enable html
    format_layout_part(label)
    return label