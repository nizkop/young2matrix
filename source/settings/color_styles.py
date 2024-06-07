from enum import Enum


class color_styles(Enum):
    """
    different choices of color schemes for the display of the GUI
    ! sorely UI relevant class
    """
    DEFAULT = {"name": "default",
               "text": "black",
               "status_text": "white",
               "background": "rgb(182, 255, 145)",#B6FF91
               "status_background": "rgb(50, 120, 50)",#327832
               "button-background": "rgb(152, 225, 115)",#98E173
               # "info_background": "rgb(165, 75, 75)",
               "button-border": "rgb(30, 70, 30)",
               "deactivated-button": "#6fa287",
               "disabled-text": "rgb(169, 169, 169)"#a9a9a9
               }
    DARKMODE = {"name": "darkmode",
                "text": "rgb(208, 225, 249)",#D0E1F9
                "status_text": "black",
                "background": "rgb(99,99,99)",#636363
                "status_background": "rgb(100, 120, 150)",#647896
                "button-background": "rgb(90, 90, 90)",#5A5A5A
                # "info_background": "rgb(40, 60, 100)",
                "button-border": "rgb(60, 60, 60)",
                "deactivated-button": "rgb(169, 169, 169)", #A9A9A9
                "disabled-text": "rgb(60, 60, 60)"#3C3C3C
                }
    PLAIN = {"name": "plain",
             "background": "white",
             "text": "black",
             "status_background": "rgb(85,85,85)",#555555
             "status_text": "white",
             # "info_background": "rgb(204,0,0)",
             "button-background": "lightgrey", #D3D3D3
             "button-border": "grey",
             "deactivated-button": "rgb(169, 169, 169)",#A9A9A9
             "disabled-text": "rgb(21, 21, 21)"#151515
             }
    WARM = {"name": "warm",
            "text": "rgb(51,25,0)",#331900
            "status_text": "black",
            "background": "rgb(235, 169, 55)",#EBA937
            "status_background": "rgb(204,102,0)",#CC6600
            "button-background": "rgb(243, 229, 171)",#F3E5AB
            # "info_background": "rgb(255, 102, 51)",
            "button-border": "rgb(102,51,0)",
            "deactivated-button": "rgb(200, 190, 160)",#C8BEA0
            "disabled-text": "rgb(100, 70, 40)"#644628
            }

# https://acrylgiessen.com/farbkombinationen/
# https://www.siteimprove.com/de/toolkit/color-contrast-checker/