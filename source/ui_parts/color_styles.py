from enum import Enum


class color_styles(Enum):

    DEFAULT = {"name": "default", "background": "lightgreen", "text": "black", "status_background": "darkgreen",
               "status_text": "white", "info_background": "rgb(255, 150, 150)", "settings": "darkgreen"}
    DARKMODE = {"name": "darkmode", "background": "rgb(60,60,60)", "text": "white", "status_background": "rgb(105,105,105)",
                "status_text": "black", "info_background": "rgb(146,35,35)", "settings": "gray"}
    PLAIN = {"name": "plain", "background":  "white", "text": "black", "status_background": "gray",
               "status_text": "white", "info_background": "red", "settings": "darkred"}