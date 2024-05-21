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
    PLAIN = {"name": "plain", "background":  "white", "text": "black", "status_background": "gray",
               "status_text": "white", "info_background": "red", "settings": "darkred","button-background": "lightgrey",}

    GREEN1 = {"name": "green1", "text": "black","status_text": "white", "settings": "black",
              "background": "rgb(125, 180, 108)",
              "status_background": "rgb(135, 206, 250)",
              "button-background": "rgb(170, 213, 219)",
              "info_background": "darkred",
              }
    HONEY = {"name": "honey",  "text": "black","status_text": "white", "settings": "black",
             "background": "rgb(235, 169, 55)",
             "status_background": "rgb(172, 225, 175)",
             "button-background": "rgb(243, 229, 171)",
             "info_background": "rgb(227, 66, 52)",
             }

# https://acrylgiessen.com/farbkombinationen/


"""
#8D230F, #1E434C, #9B4F0F, #C99E10
#363237, #2D4262, #73605B 
#1E1F26, #283655, #4D648D (#D0E1F9 statt weiß)
"""