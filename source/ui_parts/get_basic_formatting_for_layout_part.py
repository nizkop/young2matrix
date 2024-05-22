from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QStatusBar, QLineEdit, QWidget, QScrollArea, QProgressBar

from source.ui_parts.settings.color_styles import color_styles
from source.ui_parts.settings.settings_config import load_config


#ApplicationWindows, SettingsDialog
def format_layout_part(layout_part: Union[QPushButton, QLabel, QMessageBox, QStatusBar, QLineEdit, QWidget, QScrollArea
    ], added_style: str = "") -> None:
    """
    setting the basic color/size/... attributes for layout parts like buttons
    :param layout_part: some kind of layout item, that needs to be colorized
    :param added_style: additional styling information (that is not added in general here)
    :return:
    """
    if type(layout_part) not in [QPushButton, QLabel, QMessageBox, QStatusBar, QLineEdit, QWidget, QScrollArea, QProgressBar]: # development only!!! todo: remove
        print(f"missing typing of: {type(layout_part)}")
    settings = load_config()
    try:
        color = color_styles[settings['color']]
    except:
        color = color_styles["DEFAULT"]

    items = [f"font-size: {settings['font-size']}pt;", f"color: {color.value['text']};", "padding: 10px;"]
    if isinstance(layout_part, QPushButton):
        for item in [f"background-color: {color.value['button-background']};", "font-weight: bold;",
                                      "border-radius: 5px;", f"border: 2px solid {color.value['button-border']} ;", ]:
            items.append(item)
    elif isinstance(layout_part, QProgressBar):
        items = [f"""
                QProgressBar {{
                    border: 2px solid {color.value['button-border']};
                    border-radius: 5px;
                    text-align: center;
                    padding: 10 px; 
                    font-size: {settings['font-size']}pt;
                }}
                QProgressBar::chunk {{
                    border-radius: 5px;
                    background-color: {color.value['status_background']};
                }}"""]#changing the color of the progress following bar inside the progress bar  /* color: {color.value['text']}; */
    else:
        items.append(f"background-color: {color.value['background']};")

    style = ""
    for item in items:
        if item[:item.find(":")].replace(" ","") not in added_style:
            style+=item
    layout_part.setStyleSheet(style+added_style)


def get_contrast_color(background_color: str) -> str:
    print("get_contrast_color", flush=True)
    # Farbe in ein QColor-Objekt umwandeln
    background_qcolor = QColor(background_color)

    # Helligkeit des Hintergrunds berechnen (YIQ-Formel)
    yiq = ((background_qcolor.red() * 299) + (background_qcolor.green() * 587) + (
                background_qcolor.blue() * 114)) / 1000

    # Kontrastfarbe basierend auf der Helligkeit wählen
    return "black" if yiq >= 128 else "white"