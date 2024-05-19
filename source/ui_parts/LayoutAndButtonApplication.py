
from typing import Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QScrollArea, QStatusBar, QMessageBox, \
    QApplication, QSpacerItem, QSizePolicy

from source.texts.general_texts import get_general_text
from source.texts.get_page_information import get_page_information
from source.ui_parts.color_styles import color_styles
from source.ui_parts.settings.language_choices import language_choices
from source.ui_parts.ui_pages import get_page_name
from source.ui_parts.settings.idea_config import update_language, get_language
from source.ui_parts.SettingsDialog import SettingsDialog
from source.ui_parts.get_colored_icon_button import get_colored_icon_button


class LayoutAndButtonApplication(QMainWindow):
    """ basic setup for application (only a parent class, because it would become too large to keep track)
    = Subclass Responsibility;
    this sets up the general structure and format of the screen, including the general buttons settings and info as well as the information bar at the bottom
    (actual content in the middle of the screen is not added yet)
    """
    def __init__(self):
        super().__init__()

        self.color = color_styles.DEFAULT #color_styles.DEFAULT
        self.setGeometry(100, 100, 800, 600)
        self.top_y = 5
        self.margin_x = 5
        self.button_size = 30

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        top_spacer = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout.addItem(top_spacer)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.statusBar = QStatusBar()#information about button functions
        self.setStatusBar(self.statusBar)#(shown at the bottom of the screen)
        self.statusBar.setStyleSheet(f"color: {self.color.value['text']};")

        self.setStyleSheet(f"background-color: {self.color.value['background']}; font-size: 15pt;")

        self.settings_button = None
        self.create_settings_button()
        self.create_help_button()

    def create_settings_button(self) -> None:
            """ adding a button, that may change the settings, to the top of the screen """
            # print("create_settings_button",flush=True)
            if self.settings_button is None:
                self.settings_button = QPushButton()
                self.settings_button.setFixedSize(self.button_size, self.button_size)
                self.settings_button.move(self.margin_x, self.top_y)

                # ! activates Button each time it is called -> potentially raising number of clicks needed to get
                # rid of button if ths line is called every time create_settings_button is called:
                self.settings_button.clicked.connect(self.open_settings)

            self.settings_button = get_colored_icon_button(button=self.settings_button, file_path="./source/ui_parts/settings/icons8-settings.svg",
                                                           color=self.color.value["settings"])

            self.settings_button.setStyleSheet(f"background-color: {self.color.value['background']}; color: {self.color.value['text']}; font-weight: bold; font-size: 15pt;")


            self.settings_button.setToolTip(get_general_text("settings_change"))
            self.settings_button.enterEvent = lambda event, button= self.settings_button: self.change_status_message( self.settings_button.toolTip())
            self.settings_button.leaveEvent = lambda event: self.change_status_message()

            self.settings_button.setParent(self)

    def open_settings(self) -> None:
        """
        opening a separate ui box for the settings dialog
        :return:
        """
        # print("open_settings",flush=True)
        dialog = SettingsDialog(self.color)
        if dialog.exec_():
            selected_color = dialog._selected_color()
            for color in color_styles:
                if selected_color == color.value["name"]:
                    if color != self.color:
                        self.color = color
                        self.setStyleSheet(f"background-color: {color.value['background']};")
                        self.change_status_message()  # change background color in case of changed color
                        # self.create_settings_button()

            selected_language = dialog._selected_language()
            self.set_language(selected_language)

            self.change_page(self.current_page)#update colors/...
            # self.settings_button.clicked.connect(self.open_settings)

    def create_help_button(self) -> None:
        """
        setting up a belp button, where more information about the content of the actual page/screen is shown
        :return:
        """
        help_button = QPushButton("?", self)
        help_button.setFixedSize(self.button_size, self.button_size)
        help_button.move(self.width()-self.margin_x-self.button_size,self.top_y)#x, y
        help_button.setStyleSheet(f"background-color: {self.color.value['info_background']}; color: {self.color.value['text']}; border-radius: {self.button_size//2}; border :   1px   solid   grey  ")# 50 % <-> circle
        help_button.clicked.connect(self.show_info)
        help_button.enterEvent = lambda event, button=help_button:self.change_status_message(get_general_text("help"))
        help_button.leaveEvent = lambda event: self.change_status_message()
        help_button.setParent(self)

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
        update_language(language.name)
        for p in range(len(self.pages)):# update pages names
            self.pages[p]["name"] = get_page_name(self.pages[p]["index"])
        self.create_settings_button()
        self.open_page(self.current_page)

    def change_status_message(self, message:Union[str,None]=None) -> None:
        """
        giving/deleting an information at the bottom of the screen (when the mouse hovers above an item)
        :param message: information (status bar is reset to an empty space in case the message is None)
        """
        if message is None or len(message) == 0:
            self.statusBar.clearMessage()
            self.statusBar.setStyleSheet(f"background-color: {self.color.value['background']}; color: {self.color.value['text']};")
        else:
            self.statusBar.showMessage(message)
            self.statusBar.setStyleSheet(f"background-color: {self.color.value['status_background']}; color: {self.color.value['status_text']};")

    def show_info(self) -> None:
        """
        activating a separate ui box, showing the requested additional information about the acutal page
        :return:
        """
        # print("show info", flush=True)
        page_info = next((page_dict for page_dict in self.pages
                          if page_dict.get("index").value == self.current_page), None)
        if page_info is None:
            return self.change_page(0)
        # print(self.current_page, page_info)
        info = QMessageBox()
        info.setWindowTitle("INFO")
        info.setTextFormat(Qt.RichText)
        info.setText(get_page_information(page_info["index"]))
        info.setStyleSheet(f"color: {self.color.value['text']}; background-color: {self.color.value['background']};")
        info.exec_()



if __name__ == "__main__":
    app = QApplication([])
    main_view = LayoutAndButtonApplication()
    main_view.show()
    app.exec_()
