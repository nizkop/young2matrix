
'''
self.scroll_area.setStyleSheet(r"""
                    QScrollBar:vertical {
                        background: blue;
                    }
                    QScrollBar::handle:vertical {
                        background: orange;
                        margin: 15px 1px 15px 1px;  /* top, right, bottom, left */
                    }
                """)
        # self.central_widget.setStyleSheet(
        #     f"""font-size: {settings['font-size']}pt;
        #     color: black;
        #     padding: 10px;
        #     background-color: {get_color()['background']};
        #     """)
        #             QScrollBar:vertical {{
        #                     }}
        self.scroll_area.setStyleSheet(
            f"""
            font-size: {settings['font-size']}pt;
            color: black;
            padding: 10px;
            background-color: {get_color()['background']};
         """
        )
        self.scroll_area.setStyleSheet(r"""
                    QScrollBar:vertical {
                        background: blue;
                    }
                    QScrollBar::handle:vertical {
                        background: orange;
                        margin: 15px 1px 15px 1px;  /* top, right, bottom, left */
                    }
                """)
        # self.scroll_area.setStyleSheet("""
        #     QScrollBar:vertical {{
        #         background: blue;
        #     }}
        #     QScrollBar::handle:vertical {{
        #         background: orange;
        #         margin: 15px 1px 15px 1px;  /* top, right, bottom, left */
        #     }}
        #     """
        # )

        # self.scroll_area.setStyleSheet(self.get_scrollbar_colors())
'''
from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part
from source.ui_parts.settings.settings_config import load_config, get_color

settings = load_config()
color = get_color()




def tst_uptonow(self):
    format_layout_part(self.scroll_area)
    format_layout_part(self.central_widget)

def tst_separate(self):
    self.scroll_area.setStyleSheet(
        f"""
        font-size: {settings['font-size']}pt; 
        color: black; 
        padding: 10px;
        background-color: {color['background']};
     """
    )
    self.scroll_area.setStyleSheet(get_scrollbar_colors())

def tst_common(self):
    # self.scroll_area.setStyleSheet(
    #     f"""
    #     font-size: {settings['font-size']}pt;
    #     color: black;
    #     padding: 10px;
    #     background-color: {get_color()['background']};
    #     """
    # )
    # self.scroll_area.setProperty("background", "blue")
    # self.scroll_area.verticalScrollBar().setProperty("background", "blue")
    # self.scroll_area.verticalScrollBar().setProperty("handle-background", "orange")
    # self.scroll_area.verticalScrollBar().setProperty("handle-margin", "15px 1px 15px 1px")
    self.scroll_area.setStyleSheet(get_scrollbar_colors())
    self.scroll_area.setProperty("background-color", get_color()['background'])


def tst_csv(self):
    # format_layout_part(self.central_widget)

    self.central_widget.setStyleSheet(f"""background-color: {color['background']}; """)#working
    self.central_widget.setStyleSheet(f"""background-color: {color['background']}; 
        font-size: {settings['font-size']}pt;""")#working
    self.central_widget.setStyleSheet(f"""background-color: {color['status_background']}; 
        font-size: {settings['font-size']}pt;
        color: {color['text']};""")#working
    # self.central_widget.setStyleSheet(f"""background-color: {color['background']};
    # font-size: {settings['font-size']}pt;
    # color: {color['text']};
    # padding: 10px;""")#not working

    with open("styles.css", "r") as f:
        css = f.read()
    self.scroll_area.setStyleSheet(css)

def tst_limited(self):
    format_layout_part(self.central_widget)
    format_layout_part(self.scroll_area)
    # self.scroll_area.setStyleSheet(get_scrollbar_colors())
