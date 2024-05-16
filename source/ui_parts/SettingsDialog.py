from PyQt5.QtWidgets import QComboBox, QDialog, QVBoxLayout, QPushButton, QLabel

from source.texts.general_texts import get_general_text
from source.ui_parts.color_styles import color_styles
from source.ui_parts.settings.idea_config import get_language
from source.ui_parts.settings.language_choices import language_choices


class SettingsDialog(QDialog):
    def __init__(self, colorscheme:color_styles):
        super().__init__()
        self.color_scheme = colorscheme

        self.layout = QVBoxLayout()
        self.setStyleSheet(f"background-color: {colorscheme.value['background']}; color: {colorscheme.value['text']}; font-size: 15pt;")

        self.create_language_button()
        self.create_colorscheme_button()
        self.create_confirm_button()

        self.setLayout(self.layout)

    def create_colorscheme_button(self):
        colorscheme_label = QLabel(get_general_text("choose_color"))
        self.layout.addWidget(colorscheme_label)

        self.input_colorscheme = QComboBox()
        for color in color_styles:
            self.input_colorscheme.addItem(color.value["name"])
        self.input_colorscheme.setCurrentText(self.color_scheme.value["name"])
        self.layout.addWidget(self.input_colorscheme)

    def create_language_button(self):
        language_label = QLabel(get_general_text("choose_language"))
        self.layout.addWidget(language_label)

        self.input_language = QComboBox()
        for language in language_choices:
            self.input_language.addItem(language.value)
        # print([choice for choice in language_choices], [choice.name for choice in language_choices], get_language())
        choice = [choice for choice in language_choices if choice.name == get_language()]
        if len(choice) == 0:
            choice = [language_choices.de]#default
        self.input_language.setCurrentText(choice[0].value)
        self.layout.addWidget(self.input_language)

    def create_confirm_button(self):
        self.confirm_button = QPushButton("OK")
        self.layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.accept)


    def selected_color(self):
        """Returns selected color as string of name """
        # print("selected_color",flush=True)
        return self.input_colorscheme.currentText()

    def selected_language(self):
        # print("selected_language",flush=True)
        return self.input_language.currentText()

