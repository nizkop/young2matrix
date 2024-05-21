from typing import Union

from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QStatusBar, QLineEdit, QWidget, QScrollArea

from source.ui_parts.settings.color_styles import color_styles
from source.ui_parts.settings.language_config import load_config


#ApplicationWindows, SettingsDialog
def format_layout_part(layout_part: Union[QPushButton, QLabel, QMessageBox, QStatusBar, QLineEdit, QWidget, QScrollArea
    ], added_style: str = "") -> None:
    if type(layout_part) not in [QPushButton, QLabel, QMessageBox, QStatusBar, QLineEdit, QWidget, QScrollArea]: # development only!!! todo: remove
        print(f"missing typing of: {type(layout_part)}")
    settings = load_config()
    # try:
    color = color_styles[settings['color']]
    # except:
    #     color = color_styles["DEFAULT"]

    items = [f"font-size: {settings['font-size']}pt;", f"color: {color.value['text']};","padding: 10px;"]
    if isinstance(layout_part, QPushButton):
        for item in [f"background-color: {color.value['button-background']};", "font-weight: bold;",
                                      "border-radius: 5px;", f"border: 2px solid {color.value['button-border']} ;", ]:
            items.append(item)
    else:
        items.append(f"background-color: {color.value['background']};")

    style = ""
    for item in items:
        if item[:item.find(":")].replace(" ","") not in added_style:
            style+=item
    layout_part.setStyleSheet(style+added_style)
