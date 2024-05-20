from typing import Union

from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel

from source.ui_parts.settings.color_styles import color_styles
from source.ui_parts.settings.language_config import load_config


def format_layout_part(layout_part: Union[QPushButton, QLabel, QMessageBox], added_style: str = "") -> None:
    settings = load_config()
    try:
        color = color_styles[settings['color']]
    except:
        color = color_styles["DEFAULT"]
    if isinstance(layout_part, QPushButton):
        items = [f"background-color: {color.value['background']};", "font-weight: bold;",
                                      f" font-size: {settings['button-font-size']}pt;",
                                      f"color: {color.value['text']};","border-radius: 5px;",
                                      f"border :   2px   solid   grey ; "]
    # if isinstance(button_or_label, QMessageBox):
    #     button_or_label.setStyleSheet(
    #         f"color: {self.color.value['text']}; background-color: {self.color.value['background']};")
    else:#QMessageBox, QLabel
        items = [f"font-size: {settings['font-size']}pt; ","color: {color.value['text']}; ",
            f"background-color: {color.value['background']};"]

    style = ""
    for item in items:
        if item[:item.find(":")].replace(" ","") not in added_style:
            style+=item
    print(layout_part, style)
    layout_part.setStyleSheet(style+added_style)
