from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton

#
# class CustomDialog(QDialog):
#     def __init__(self, content="",parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Warning")
#         self.setFixedSize(400, 200)
#
#         self.label = QLabel(content, self)
#         layout = QHBoxLayout(self)
#         self.setLayout(layout)
#
#     def add_button(self, button):
#         """Add a button to the dialog."""
#         self.layout().addWidget(button)

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel

from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part
from source.ui_parts.small_basic_parts.get_basic_push_button import get_basic_push_button


class FormatableMessageBox(QDialog):
    """
    needed primarily to format the buttons
    """
    def __init__(self, window_title:str="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.setFixedSize(400, 200)
        format_layout_part(self)

        layout = QVBoxLayout(self)

        self.label = QLabel("", self)#dummy label text
        self.label.setWordWrap(True)
        self.label.setMaximumWidth(self.width())
        self.label.setTextFormat(Qt.RichText)
        layout.addWidget(self.label)

        self.button_layout = QHBoxLayout()
        self.layout().addLayout(self.button_layout)
        self.set_buttons = False

    def setText(self, content:str) -> None:
        """
        setting the correct text for the message box
        :param content: html formatted information
        :return:
        """
        self.label.setText(content)

    def add_button(self, button: QPushButton) -> None:
        """ adding a button
        :param button: readily formatted/... button """
        self.set_buttons = True
        self.button_layout.addWidget(button)

    def exec_(self, *args, **kwargs) -> None:
        """
        trigger execution after ensuring, that at least one button exists
        """
        if not self.set_buttons:
            ok_button = get_basic_push_button("OK")
            ok_button.clicked.connect(self.accept)
            format_layout_part(ok_button)
            self.add_button(ok_button)
        super().exec_(*args, **kwargs)


