from PyQt5.QtWidgets import QComboBox, QDialog, QVBoxLayout

from source.settings.settings_config import load_config, get_color, get_language
from source.texts.general_texts import get_general_text
from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part
from source.ui_parts.small_basic_parts.get_basic_label import get_basic_label
from source.ui_parts.small_basic_parts.get_basic_push_button import get_basic_push_button
from source.settings.color_styles import color_styles
from source.settings.language_choices import language_choices


class SettingsDialog(QDialog):
    """
    this is the actual settings dialog box (accessible on each page)
    (aside from the initiation, this class/its methods are not used)
    """
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        format_layout_part(self)

        self.create_language_button()
        self.create_colorscheme_button()
        self.create_confirm_button()

        self.setLayout(self.layout)

    def create_colorscheme_button(self) -> None:
        """ setting up a single-choice button to choose a color scheme for the ui display """
        colorscheme_label = get_basic_label(get_general_text("choose_color"), self.width())# does not set a fixed width!
        colorscheme_label.setMinimumWidth(load_config()["geometry"][2]//2)# half of main appl. width
        self.layout.addWidget(colorscheme_label)

        self.input_colorscheme = QComboBox()
        for color in color_styles:
            self.input_colorscheme.addItem(color.value["name"])
        self.input_colorscheme.setCurrentText(get_color()["name"])
        self.layout.addWidget(self.input_colorscheme)

    def create_language_button(self) -> None:
        """ setting up a single-choice button to choose a language (choice persistently saved in settings file) """
        language_label = get_basic_label(get_general_text("choose_language"), self.width())
        language_label.setMinimumWidth(load_config()["geometry"][2]//2)# half of main appl. width!
        self.layout.addWidget(language_label)

        self.input_language = QComboBox()
        for language in language_choices:
            self.input_language.addItem(language.value)
        choice = [choice for choice in language_choices if choice.name == get_language()]
        if len(choice) == 0:
            choice = [language_choices.de]#default
        self.input_language.setCurrentText(choice[0].value)
        self.layout.addWidget(self.input_language)

    def create_confirm_button(self) -> None:
        """ setting up the confirm button to save and exit the settings dialog """
        self.confirm_button = get_basic_push_button("OK")
        format_layout_part(self.confirm_button)
        self.layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.accept)

    def _selected_color(self) -> str:
        """ private method, that returns selected color as string of name """
        # print("selected_color",flush=True)
        return self.input_colorscheme.currentText()

    def _selected_language(self) -> str:
        """ private method, that return selected language as string of name """
        # print("selected_language",flush=True)
        return self.input_language.currentText()

