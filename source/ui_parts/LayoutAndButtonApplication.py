from typing import Union
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QScrollArea, QStatusBar, QApplication

from source.texts.general_texts import get_general_text
from source.texts.get_page_information import get_page_information
from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part
from source.ui_parts.small_basic_parts.get_basic_push_button import get_basic_push_button
from source.ui_parts.settings.color_styles import color_styles
from source.ui_parts.settings.language_choices import language_choices
from source.ui_parts.ui_pages import get_page_name
from source.ui_parts.settings.settings_config import update_settings, get_language, load_config, get_color
from source.ui_parts.SettingsDialog import SettingsDialog
from source.ui_parts.small_basic_parts.get_colored_icon_button import get_colored_icon_button
from source.ui_parts.FormatableMessageBox import FormatableMessageBox


class LayoutAndButtonApplication(QMainWindow):
    """ basic setup for application (only a parent class, because it would become too large to keep track)
    = Subclass Responsibility;
    this sets up the general structure and format of the screen, including the general buttons settings and info as well as the information bar at the bottom
    (actual content in the middle of the screen is not added yet)
    """
    def __init__(self):
        super().__init__()
        settings = load_config()
        x, y, width, height = settings["geometry"]
        self.setGeometry(x, y, width, height)
        self.spacer_height = settings["button-size"] + 2 * settings["margin-top-y"]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        format_layout_part(self.central_widget)
        self.top_spacer = QWidget()# spacer as widget to change background color
        self.top_spacer.setFixedHeight(self.spacer_height)
        format_layout_part(self.top_spacer)
        self.top_spacer.setStyleSheet(f"background-color: {get_color()['status_background']};")
        self.layout.addWidget(self.top_spacer)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        format_layout_part(self.scroll_area)

        self.layout.addWidget(self.scroll_area)# !! setStylesheet before adding it to something

        self.statusBar = QStatusBar()#information about button functions
        self.setStatusBar(self.statusBar)#(shown at the bottom of the screen)
        format_layout_part(self.statusBar)#f"color: {self.color.value['text']};")

        self.settings_button = None
        self.create_settings_button()
        self.help_button = None
        self.create_help_button()



    def create_settings_button(self, color:str=None) -> None:
            """ adding a button, that may change the settings, to the top of the screen """
            # print("create_settings_button",flush=True)
            if color is None:
                color = get_color()["text"]
            if self.settings_button is None:
                self.settings_button = get_basic_push_button()
                self.settings_button.setFixedSize(load_config()["button-size"], load_config()["button-size"])
                self.settings_button.move(load_config()["margin-top-y"], load_config()["margin-top-y"])

                # ! activates Button each time it is called -> potentially raising number of clicks needed
                # to get rid of button if ths line is called every time create_settings_button is called:
                self.settings_button.clicked.connect(self.open_settings)

            self.settings_button = get_colored_icon_button(button=self.settings_button,
                                                           file_path="./source/ui_parts/settings/icons8-settings.svg",
                                                           color=color)
            self.settings_button.setIconSize(QSize(load_config()["button-size"], load_config()["button-size"]))
            format_layout_part(self.settings_button)
            self.settings_button.setToolTip(f"<span style='font-size:{load_config()['font-size']}pt;'>"+
                                            f"{get_general_text('settings_change')}</span>")
            self.settings_button.enterEvent = lambda event, button= self.settings_button: (
                                            self.change_status_message(get_general_text('settings_change')))
            self.settings_button.leaveEvent = lambda event: self.change_status_message()

            self.settings_button.setParent(self)

    def open_settings(self) -> None:
        """
        opening a separate ui box for the settings dialog
        :return:
        """
        # print("open_settings",flush=True)
        dialog = SettingsDialog()
        if dialog.exec_():
            selected_color = dialog._selected_color()
            for color in color_styles:
                if selected_color == color.value["name"]:
                    if color.value != get_color():
                        self.change_status_message()  # change background color in case of changed color
                        update_settings(color.name, "color")
                        format_layout_part(self.top_spacer,
                                           f"background-color: {get_color()['status_background']};")# headline
                        format_layout_part(self.central_widget)# main background
                        format_layout_part(self.scroll_area)# main background
                        format_layout_part(self.statusBar)

                        self.create_settings_button(color=color.value["text"])#update
                        # self.create_help_button()#update
                        # is called in clear_screen in change_page anyway

            selected_language = dialog._selected_language()
            self.set_language(selected_language)
            self.open_page(self.current_page)#update colors/...

    def create_help_button(self) -> None:
        """
        setting up a help button, where more information about the content of the actual page/screen is shown
        :return:
        """
        if self.help_button is None:
            self.help_button = get_basic_push_button("?")
            self.help_button.setParent(self)
            self.help_button.setFixedSize(load_config()['button-size'],load_config()['button-size'])
            self.help_button.move(self.width() - load_config()['margin-top-y'] - load_config()['button-size'],
                                  load_config()['margin-top-y'])
            self.help_button.clicked.connect(self.show_info) # ! activates the click each time this is called
        format_layout_part(self.help_button)
        self.help_button.setToolTip(f"<span style='font-size:{load_config()['font-size']}pt;'>{get_general_text('help')}</span>")
        self.help_button.enterEvent = lambda event, button=self.help_button:self.change_status_message(get_general_text("help"))
        self.help_button.leaveEvent = lambda event: self.change_status_message()
        self.help_button.setParent(self)


    def resizeEvent(self, event: QResizeEvent) -> None:
        """
         (! function needs to be called this (this is an overwrite))
        removing help button upon event:
        automatically move help button further to the right in case the screen size is changed
        """
        self.help_button.move(self.width() - (load_config()["margin-top-y"]) - load_config()["button-size"],
                              load_config()["margin-top-y"])# x, y
        event.accept()

    def set_language(self, choosen_language: language_choices) -> None:
        """ updating the language (as it was changed by the user)
        :param choosen_language: choice of a new language
        """
        # print("set language: ", [choosen_language], flush=True)
        for language in language_choices:
            if language.value == choosen_language:
                break
        if language.name == get_language():
            return
        update_settings(language.name, "language")
        for p in range(len(self.pages)):# update pages names
            self.pages[p]["name"] = get_page_name(self.pages[p]["index"])
        # self.create_settings_button()
        # self.open_page(self.current_page)

    def change_status_message(self, message:Union[str,None]=None) -> None:
        """
        giving/deleting an information at the bottom of the screen (when the mouse hovers above an item)
        :param message: information (status bar is reset to an empty space in case the message is None)
        """
        if message is None or len(message) == 0:
            format_layout_part(self.statusBar, added_style=f"background-color: {get_color()['background']};" +
                                                           f" color: {get_color()['text']};")
            self.statusBar.clearMessage()
        else:
            format_layout_part(self.statusBar, added_style=f"background-color:{get_color()['status_background']};" +
                                                           f" color: {get_color()['status_text']};")
            self.statusBar.showMessage(message)

    def show_info(self) -> None:
        """
        activating a separate ui box, showing the requested additional information about the actual page
        :return:
        """
        page_info = next((page_dict for page_dict in self.pages
                          if page_dict.get("index").value == self.current_page), None)
        if page_info is None:
            return self.change_page(0)
        info = FormatableMessageBox("INFO")
        info.setText(get_page_information(page_info["index"]))
        info.exec_()



if __name__ == "__main__":
    app = QApplication([])
    main_view = LayoutAndButtonApplication()
    main_view.show()
    app.exec_()
