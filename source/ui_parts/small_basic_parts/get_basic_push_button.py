from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton


def get_basic_push_button(content:str=None) -> QPushButton:
    """
    getting a button formatted with a shadow to mark it as clickable
    :param content: text inside the button
    :return: button object that can be added to ui
    """
    if content is None:
        button = QPushButton()
    else:
        button = QPushButton(content)
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(5)
    shadow.setOffset(2.5, 2.5)
    button.setGraphicsEffect(shadow)
    return button