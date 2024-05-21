from enum import Enum


class color_styles(Enum):
    DEFAULT = {"name": "default",
               "text": "black",
               "status_text": "white",
               "background": "rgb(182, 255, 145)",
               "status_background": "rgb(60, 140, 60)",#rgb(50, 120, 50)
               "button-background": "rgb(152, 225, 115)",
               "info_background": "rgb(165, 75, 75)",
               "button-border": "rgb(30, 70, 30)",
               }
    DARKMODE = {"name": "darkmode",
                "text": "rgb(208, 225, 249)",
                "status_text": "black",
                "background": "grey",
                "status_background": "rgb(100, 120, 150)",
                "button-background": "rgb(90, 90, 90)",
                "info_background": "rgb(40, 60, 100)",
                "button-border": "rgb(60, 60, 60)",
                }
    PLAIN = {"name": "plain",
             "background":  "white",
             "text": "black",
             "status_background": "rgb(105, 105, 105)",
             "status_text": "white",
             "info_background": "rgb(204,0,0)",
             "button-background": "lightgrey",
             "button-border": "grey"
             }
    WARM = {"name": "warm",
            "text": "rgb(51,25,0)",
            "status_text": "rgb(51,25,0)",
            "background": "rgb(235, 169, 55)",
            "status_background": "orange",
            "button-background": "rgb(243, 229, 171)",
            "info_background": "rgb(255, 102, 51)",
            "button-border": "rgb(102,51,0)"
            }

# https://acrylgiessen.com/farbkombinationen/
