import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon

from source.ui_parts.PageYoungTableau import PageYoungTableaus


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Permutationsgruppe")
        self.setGeometry(100, 100, 600, 400)  # x position, x position, width, height

        self.pages = [
            {"sign":"[1][2]", "class": PageYoungTableaus},
            {"sign": "σ", "class": PageYoungTableaus},
            {"sign": "Φ", "class": PageYoungTableaus},
        ]

        self.layout = QVBoxLayout()
        self.setStyleSheet("background-color: lightgreen;")
        self.add_input()
        self.add_buttons()

    def add_input(self):
        input_layout = QHBoxLayout()
        input_label = QLabel("Permutationsgruppe:")
        input_layout.addWidget(input_label)

        self.input_box = QLineEdit()
        input_layout.addWidget(self.input_box)

        self.layout.addLayout(input_layout)

    def add_buttons(self):
        buttons_layout = QHBoxLayout()

        for i, sign in enumerate( [page.get("sign", "") for page in self.pages if "sign" in page] ):
            button = QPushButton(sign)
            buttons_layout.addWidget(button)

            if i == 0:
                button.clicked.connect(self.open_page)
                # self.pages[i]["class"](self)

        download_button = QPushButton("")
        download_button.setIcon(QIcon.fromTheme("document-save"))
        buttons_layout.addWidget(download_button)

        self.layout.addLayout(buttons_layout)

        self.setLayout(self.layout)

    def clearLayout(self):
        """ clearing the current layout"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    def back_to_start(self):
        self.clearLayout()
        self.add_input()
        self.add_buttons()


    def open_page(self):
        self.clearLayout()
        # getting the input information:
        input_value = self.input_box.text()
        if not input_value:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine Permutationsgruppe ein.")
            return
        try:
            input_value = int(input_value)
            if input_value <= 0:
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine Permutationsgruppe als positive Zahl.")
                return
        except:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie die Nummer für eine Permutationsgruppe ein.")
            return
        # PageYoungTableaus(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())