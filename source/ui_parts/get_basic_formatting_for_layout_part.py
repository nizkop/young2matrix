from typing import Union
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QStatusBar, QLineEdit, QWidget, QScrollArea, QProgressBar

from source.settings.GLOBALS import FONT_SIZE, BUTTON_ROUNDING, BUTTON_LINE, BUTTON_SIZE
from source.settings.settings_config import load_config
from source.ui_parts.get_scrollbar_colors import get_scrollbar_colors, Directions
from source.settings.ColorStyles import ColorStyles


#also uses: (ApplicationWindows), SettingsDialog, FormatableMessageBox
def format_layout_part(layout_part: Union[QPushButton, QLabel, QMessageBox, QStatusBar, QLineEdit, QWidget, QScrollArea
    ], added_style: str = "") -> None:
    """
    setting the basic color/size/... attributes for layout parts like buttons
    :param layout_part: some kind of layout item, that needs to be colorized
    :param added_style: additional styling information (that is not added in general here)
    :return:
    """
    settings = load_config()
    try:
        color = ColorStyles[settings['color']]
    except:
        color = ColorStyles["PLAIN"]

    if isinstance(layout_part, QScrollArea):
        layout_part.verticalScrollBar().setStyleSheet(get_scrollbar_colors(Directions.v))
        layout_part.horizontalScrollBar().setStyleSheet(get_scrollbar_colors(Directions.h))
        return


    items = [f"font-size: {FONT_SIZE}pt;", f"color: {color.value['text']};",
             f"padding: {BUTTON_ROUNDING*2}px;"]
    if isinstance(layout_part, QPushButton):
        if layout_part.text() =="?":
            added_style += f"border-radius: {BUTTON_SIZE // 2}; "  # 50 % <-> circle
            added_style += f"border: {BUTTON_LINE}px solid {color.value['button-border']} ;"# <- vanishes from default because of set 'border'
        for item in [f"background-color: {color.value['button-background']};", "font-weight: bold;",
                                      f"border-radius: {BUTTON_ROUNDING}px;",
                     f"border: {BUTTON_LINE}px solid {color.value['button-border']} ;",]:
            items.append(item)
    elif isinstance(layout_part, QProgressBar):
        items = [f"""
                QProgressBar {{
                    border: {BUTTON_LINE}px solid {color.value['button-border']};
                    border-radius: {BUTTON_ROUNDING}px;
                    text-align: center;
                    padding: {BUTTON_ROUNDING*2} px;
                    font-size: {FONT_SIZE}pt;
                }}
                QProgressBar::chunk {{
                    border-radius: {BUTTON_ROUNDING}px;
                    background-color: {color.value['status_background']};
                }}
                """
                ]#changing the color of the progress following bar inside the progress bar  /* color: {color.value['text']}; */)
    elif type(layout_part) == QWidget:# no subclass!
        # (-> just concerns the main area, that somehow can not have a padding, or it inhibits formatting of the scroll-bar)
        items = [f"font-size: {FONT_SIZE}pt;", f"color: {color.value['text']};",
                 f"background-color: {color.value['background']};"]
    else:
        items.append(f"background-color: {color.value['background']};")

    style = ""
    for item in items:
        if item[:item.find(":")].replace(" ","") not in added_style:
            style+=item

    layout_part.setStyleSheet(style+added_style)
