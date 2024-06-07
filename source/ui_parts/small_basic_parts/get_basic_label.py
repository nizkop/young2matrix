from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part


def get_basic_label(content:str, allowed_width:int, added_style:str = "") -> QLabel:
    """
    getting a set-up label
    :param added_style:
    :param content: e.g. html formatted text
    :param allowed_width: fixed maximal width where the line needs to break
    :return: ui label, that can be added to a layout
    """
    if not "<" in content:
        label = QLabel(f"<p> {content} </p>")
    else:
        label = QLabel(content)
    label.setWordWrap(True)#ensure line break...
    label.setMaximumWidth(allowed_width)#...at fixed width
    label.setTextFormat(Qt.RichText)#enable html
    format_layout_part(label,added_style=added_style)
    return label
