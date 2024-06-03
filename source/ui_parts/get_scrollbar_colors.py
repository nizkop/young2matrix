from enum import Enum

from source.settings import get_color

class directions(Enum):
    """ choices of ui directions (e.g. scroll bar);
    not used much, but class prevents spelling mistakes (s. get_scrollbar_colors)"""
    h = "horizontal"
    v = "vertical"


def get_scrollbar_colors(kind:directions) -> str:
    """
    getting the special formatting for the scroll bars
    :param kind: choice of vertical/horizontal scrollbar by string
    :return: styling information
    """
    color = get_color()
    return rf"""
                QScrollBar:{kind.value} {{
                    background: {color['background']};;
                }}
                QScrollBar::handle:{kind.value} {{
                    background: {color['status_background']};
                    border-radius: 4px;
                    margin: {'15px 1px 15px 1px' if kind == directions.v else '1px 15px 1px 15px'};  /* top, right, bottom, left */
                }}
            """
