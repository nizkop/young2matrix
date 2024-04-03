import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, \
    QMessageBox, QScrollArea
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from source.ui_parts.PageYoungTableau import PageYoungTableaus


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Permutationsgruppe")
        self.setGeometry(100, 100, 600, 400)  # x position, x position, width, height

        self.pages = [
            {"sign":"[1][2]", "class": PageYoungTableaus},
            {"sign": "σ", "class": PageYoungTableaus},#TODO
            {"sign": "Φ", "class": PageYoungTableaus},#TODO
        ]

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_widget = QWidget()
        scroll_area.setWidget(main_widget)

        self.layout = QVBoxLayout(main_widget)
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
            button.clicked.connect(lambda checked, page_number=i: self.open_page(page_number=page_number))

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


    def open_page(self, page_number:int):
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
        self.pages[page_number]["class"](permutation_group=input_value, parent=self)

    def add_equation(self, eq:str):
        """
        :param eq: latex-formatted equation, e.g.r"\frac{1}{2} \cdot \pi"
        """
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.text(0.05, 0.5, # <- positioning
                     rf"${eq}$", horizontalalignment='center', verticalalignment='center', fontsize=20)
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())